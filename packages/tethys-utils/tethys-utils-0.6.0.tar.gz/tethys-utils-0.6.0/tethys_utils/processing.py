#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:31:09 2021

@author: mike
"""
import xarray as xr
import numpy as np
import zstandard as zstd
import pandas as pd
import copy
import orjson
from hashlib import blake2b
from tethys_data_models.dataset import Dataset, DatasetBase, Station, Stats, StationBase
# from data_models import Geometry, Dataset, DatasetBase, Station, Stats, StationBase
from tethys_utils.misc import make_run_date_key, grp_ts_agg
# from misc import make_run_date_key, grp_ts_agg, write_pkl_zstd
import geojson
from shapely.geometry import shape, mapping, box, Point, Polygon
from shapely import wkb
from tethysts import Tethys, utils
from time import sleep

############################################
### Parameters

base_ds_fields = ['feature', 'parameter', 'method', 'product_code', 'owner', 'aggregation_statistic', 'frequency_interval', 'utc_offset']

agg_stat_mapping = {'mean': 'mean', 'cumulative': 'sum', 'continuous': None, 'maximum': 'max', 'median': 'median', 'minimum': 'min', 'mode': 'mode', 'sporadic': None, 'standard_deviation': 'std', 'incremental': 'cumsum'}

############################################
### Functions


def extract_data_dimensions(data, parameter):
    """

    """
    data_index = data[parameter].dims
    vars2 = list(data.variables)
    vars3 = [v for v in vars2 if v not in data_index]

    vars_dict = {}
    for v in vars3:
        index1 = data[v].dims
        vars_dict[v] = index1

    ancillary_variables = [v for v, i in vars_dict.items() if (i == data_index) and (v != parameter)]

    main_vars = [parameter] + ancillary_variables

    return data_index, vars3, main_vars, ancillary_variables, vars_dict


def data_integrety_checks(data, parameter, ds_metadata, attrs, encoding):
    """

    """
    # data dimensions
    data_index, vars1, main_vars, ancillary_variables, vars_dict = extract_data_dimensions(data, parameter)

    result_type = ds_metadata['result_type']
    geo_type = ds_metadata['geometry_type']
    grouping = ds_metadata['grouping']

    if ('geometry' in data_index) and (result_type == 'grid'):
        raise ValueError('You have passed geometry as an index, but the result_type is labeled as grid...something is inconsistent.')
    elif (result_type == 'time_series') and (('lon' in data_index) or ('lat' in data_index)):
        raise ValueError('You have passed lon/lat as an index, but the result_type is labeled as time_series...something is inconsistent.')

    if result_type == 'time_series':
        ts_index_list = ['geometry', 'time', 'height']
    elif result_type == 'grid':
        ts_index_list = ['lon', 'lat', 'time', 'height']
    else:
        raise ValueError('spatial_distribution should be either sparse or grid.')

    ts_essential_list = [parameter]

    ts_no_attrs_list = ['modified_date', 'station_id', 'lat', 'lon', 'name', 'altitude', 'ref', 'virtual_station', 'geometry', 'station_geometry']

    for c in ts_index_list:
        if not c in data_index:
            raise ValueError('The Data must contain the dimension: ' + str(c))

    if isinstance(attrs, dict):
        attrs_keys = list(attrs.keys())
        for col in vars1:
            if not col in ts_no_attrs_list:
                if not col in ts_essential_list:
                    if not col in attrs_keys:
                        raise ValueError('Not all columns are in the attrs dict')
    else:
        raise TypeError('attrs must be a dict')

    if isinstance(encoding, dict):
        for col in vars1:
            if not col in ts_no_attrs_list:
                if col in ancillary_variables:
                    if not col in encoding:
                        raise ValueError(col + ' must be in the encoding dict')

    ## Geometry and metadata checks
    if 'geometry' in data_index:
        data_result_type = 'time_series'
        hex_geo1 = np.unique(data['geometry'])
        if len(hex_geo1) == 1:
            data_grouping = 'none'
        else:
            data_grouping = 'blocks'

        data_geometry = wkb.loads(hex_geo1[0], True)
        data_geo_type = data_geometry.type
    elif ('lon' in data_index) and ('lat' in data_index):
        data_result_type = 'grid'
        data_geo_type = 'Point'
        lons = np.unique(data['lon'])
        lats = np.unique(data['lat'])
        if (len(lons) == 1) and (len(lats) == 1):
            data_grouping = 'none'
        else:
            data_grouping = 'blocks'
    else:
        raise ValueError('Data is not indexed correctly.')

    # Check for station_id
    if (data_grouping != 'blocks') and (result_type != 'grid'):
        if 'station_id' not in vars1:
            raise ValueError('If the grouping is not blocks and/or result_type is not grid, then the station_id should be in the data.')

    if data_geo_type != geo_type:
        raise ValueError('The data geometry type does not match the geometry type listed in the dataset metadata.')
    if data_grouping != grouping:
        raise ValueError('The data grouping does not match the grouping listed in the dataset metadata.')
    if data_result_type != result_type:
        raise ValueError('The data spatial distribution does not match the result_type listed in the dataset metadata.')

    return data.copy()


def package_xarray(data, parameter, attrs, encoding, run_date=None, compression=False, compress_level=1):
    """
    Converts DataFrames of time series data, station data, and other attributes to an Xarray Dataset. Optionally has Zstandard compression.

    Parameters
    ----------
    results_data : DataFrame
        DataFrame of the core parameter and associated ancillary variable. If the spatial distribution is sparse then the data should be indexed by geometry, time, and height. If the spatial distribution is grid then the data should be indexed by lon, lat, time, and height.
    station_data : dict
        Dictionary of the station data. Should include a station_id which should be a hashed string from blake2b (digest_size=12) of the geojson geometry. The other necessary field is geometry, which is the geometry of the results object is not grouped or a boundary extent as a polygon if the results object is grouped. Data owner specific other fields can include "ref" for the reference id and "name" for the station name.
    param_name : str
        The core parameter name of the column in the results_data DataFrame.
    results_attrs : dict
        A dictionary of the xarray/netcdf attributes of the results_data. Where the keys are the columns and the values are the attributes. Only necessary if additional ancilliary valiables are added to the results_data.
    results_encoding : dict
        A dictionary of the xarray/netcdf encodings for the results_data.
    station_attrs : dict or None
        Similer to results_attr, but can be omitted if no extra fields are included in station_data.
    station_encoding : dict or None
        Similer to results_encoding, but can be omitted if no extra fields are included in station_data.

    Returns
    -------
    Xarray Dataset or bytes object
    """
    ## dataset metadata
    ds_metadata = attrs[parameter]
    result_type = ds_metadata['result_type']
    grouping = ds_metadata['grouping']
    geo_type = ds_metadata['geometry_type']

    ## Integrity Checks
    data1 = data_integrety_checks(data, parameter, ds_metadata, attrs, encoding)

    ## data dimensions
    data_index, vars1, main_vars, ancillary_variables, vars_dict = extract_data_dimensions(data, parameter)

    ## Create extent and station_id if sd == grid
    if grouping == 'blocks':
        if 'station_id' not in data1:
            if result_type == 'grid':
                res = np.mean(np.diff(np.unique(data1['lon'])))
                min_x = (data1['lon'].min() - (res*0.5)).round(7)
                max_x = (data1['lon'].max() + (res*0.5)).round(7)
                min_y = (data1['lat'].min() - (res*0.5)).round(7)
                max_y = (data1['lat'].max() + (res*0.5)).round(7)
            else:
                raise NotImplementedError('Need to implement lines and polygons blocks extents.')
                # geos1 = [wkb.loads(g, True) for g in data1['geometry'].values]
                # TODO: Finish the lines and polygon extent creation

            extent = box(min_x, min_y, max_x, max_y)
            if not extent.is_valid:
                    raise ValueError(str(extent) + ': This shapely geometry is not valid')
            stn_id = assign_station_id(extent)
            extent_hex = extent.wkb_hex
            data1 = data1.assign_coords({'station_geometry': [extent_hex]})
            data1 = data1.assign({'station_id': (('extent'), [stn_id])})
    elif grouping == 'none':
        if 'station_id' not in data1:
            if result_type == 'grid':
                lat = round(float(data1['lat'].values[0]), 5)
                lon = round(float(data1['lon'].values[0]), 5)
                geometry = Point([lon, lat])
                if not geometry.is_valid:
                    raise ValueError(str(geometry) + ': This shapely geometry is not valid')
                stn_id = assign_station_id(geometry)
                data1 = data1.assign({'station_id': (('lon', 'lat'), [[stn_id]])})

    ## Assign lon/lat for point geometries
    if (geo_type == 'Point') and ('geometry' in data1):
        if ('lat' not in data1) or ('lon' not in data1):
            geo1 = [wkb.loads(str(g), True) for g in data1.geometry.values]
            data1 = data1.assign({'lat': (('geometry'), [g.y for g in geo1])})
            data1 = data1.assign({'lon': (('geometry'), [g.x for g in geo1])})

    ## Assign Attributes
    attrs1 = {'station_id': {'cf_role': "timeseries_id"}, 'lat': {'standard_name': "latitude", 'units': "degrees_north"}, 'lon': {'standard_name': "longitude", 'units': "degrees_east"}, 'altitude': {'standard_name': 'surface_altitude', 'long_name': 'height above the geoid to the lower boundary of the atmosphere', 'units': 'm'}, 'geometry': {'long_name': 'The hexadecimal encoding of the Well-Known Binary (WKB) geometry', 'crs_EPSG': 4326}, 'station_geometry': {'long_name': 'The hexadecimal encoding of the Well-Known Binary (WKB) station geometry', 'crs_EPSG': 4326}, 'height': {'standard_name': 'height', 'long_name': 'vertical distance above the surface', 'units': 'm', 'positive': 'up'}, 'time': {'standard_name': 'time', 'long_name': 'start_time'}, 'name': {'long_name': 'station name'}, 'ref': {'long_name': 'station reference id given by the owner'}, 'modified_date': {'long_name': 'last modified date'}, 'band': {'long_name': 'band number'}}

    if isinstance(attrs, dict):
        for k, v in attrs.items():
            x = copy.deepcopy(v)
            for w in v:
                if isinstance(v[w], list):
                    bool1 = all([isinstance(i, (int, float, str)) for i in v[w]])
                    if bool1:
                        x[w] = ' '.join(v[w])
                    else:
                        x.pop(w)
                elif not isinstance(v[w], (int, float, str)):
                    x.pop(w)
            attrs1[k] = x

    if 'cf_standard_name' in attrs1[parameter]:
        attrs1[parameter]['standard_name'] = attrs1[parameter].pop('cf_standard_name')

    if isinstance(ancillary_variables, list):
        if len(ancillary_variables) > 0:
            attrs1[parameter].update({'ancillary_variables': ' '.join(ancillary_variables)})

    # Add final attributes
    for a, val in attrs1.items():
        if a in data1:
            data1[a].attrs = val

    ## Assign encodings
    encoding1 = {'lon': {'dtype': 'int32', '_FillValue': -999999, 'scale_factor': 0.0000001}, 'lat': {'dtype': 'int32', '_FillValue': -999999, 'scale_factor': 0.0000001}, 'altitude': {'dtype': 'int32', '_FillValue': -9999, 'scale_factor': 0.001}, 'time': {'_FillValue': -99999999, 'units': "days since 1970-01-01 00:00:00"}, 'modified_date': {'_FillValue': -99999999, 'units': "days since 1970-01-01 00:00:00"}, 'band': {'dtype': 'int8', '_FillValue': -99}}

    data1['height'] = pd.to_numeric(data1['height'].values, downcast='integer')

    if 'int' in data1['height'].dtype.name:
        height_enc = {'dtype': data1['height'].dtype.name}
    elif 'float' in data1['height'].dtype.name:
        height_enc = {'dtype': 'int32', '_FillValue': -999999, 'scale_factor': 0.001}
    else:
        raise TypeError('height should be either an int or a float')

    encoding1.update({'height': height_enc})

    # Add user-defined encodings
    if isinstance(encoding, dict):
        for k, v in encoding.items():
            encoding1[k] = v

    # Add encodings
    for e, val in encoding1.items():
        if e in data1:
            if ('dtype' in val) and (not 'scale_factor' in val):
                if 'int' in val['dtype']:
                    data1[e] = data1[e].astype(val['dtype'])
            if 'scale_factor' in val:
                precision = int(np.abs(np.log10(val['scale_factor'])))
                data1[e] = data1[e].round(precision)
            data1[e].encoding = val

    ## Fix str encoding issue when the data type is object
    for v in vars1:
        if data1[v].dtype.name == 'object':
            data1[v] = data1[v].astype(str)

    ## Add top-level metadata
    title_str = '{agg_stat} {parameter} in {units} of the {feature} by a {method} owned by {owner}'.format(agg_stat=ds_metadata['aggregation_statistic'], parameter=ds_metadata['parameter'], units=ds_metadata['units'], feature=ds_metadata['feature'], method=ds_metadata['method'], owner=ds_metadata['owner'])

    run_date_key = make_run_date_key(run_date)
    data1.attrs = {'result_type': result_type, 'title': title_str, 'institution': ds_metadata['owner'], 'license': ds_metadata['license'], 'source': ds_metadata['method'], 'history': run_date_key + ': Generated', 'version': 4}

    ## Test conversion to netcdf
    p_ts1 = data1.to_netcdf()

    ## Compress if requested
    if compression:
        while True:
            cctx = zstd.ZstdCompressor(level=compress_level)
            c_obj = cctx.compress(p_ts1)

            # Test compression
            try:
                _ = utils.read_pkl_zstd(c_obj)
                break
            except:
                print('ztsd compression failure.')
                sleep(1)

        return c_obj
    else:
        return data1


def compare_dfs(old_df, new_df, on, parameter, add_old=False):
    """
    Function to compare two DataFrames with nans and return a dict with rows that have changed (diff), rows that exist in new_df but not in old_df (new), and rows  that exist in old_df but not in new_df (remove).
    Both DataFrame must have the same columns. If both DataFrames are identical, and empty DataFrame will be returned.

    Parameters
    ----------
    old_df : DataFrame
        The old DataFrame.
    new_df : DataFrame
        The new DataFrame.
    on : str or list of str
        The primary key(s) to index/merge the two DataFrames.
    parameter : str
        The parameter/column that should be compared.

    Returns
    -------
    DataFrame
        of the new dataset
    """
    if ~np.in1d(old_df.columns, new_df.columns).any():
        raise ValueError('Both DataFrames must have the same columns')

    # val_cols = [c for c in old_df.columns if not c in on]
    all_cols = new_df.columns.tolist()

    comp1 = pd.merge(old_df, new_df, on=on, how='outer', indicator=True, suffixes=('_x', ''))

    add_set = comp1.loc[comp1._merge == 'right_only', all_cols].copy()
    comp2 = comp1[comp1._merge == 'both'].drop('_merge', axis=1).copy()

    old_cols = list(on)
    old_cols_map = {c: c[:-2] for c in comp2 if '_x' in c}
    old_cols.extend(old_cols_map.keys())
    old_set = comp2[old_cols].copy()
    old_set.rename(columns=old_cols_map, inplace=True)
    new_set = comp2[all_cols].copy()

    isnull1 = new_set[parameter].isnull()
    if isnull1.any():
        new_set.loc[new_set[parameter].isnull(), parameter] = np.nan
    if old_set[parameter].dtype.type in (np.float32, np.float64):
        c1 = ~np.isclose(old_set[parameter], new_set[parameter], equal_nan=True)
    elif old_set[parameter].dtype.name == 'object':
        new_set[parameter] = new_set[parameter].astype(str)
        c1 = old_set[parameter].astype(str) != new_set[parameter]
    elif old_set[parameter].dtype.name == 'geometry':
        old1 = old_set[parameter].apply(lambda x: hash(x.wkt))
        new1 = new_set[parameter].apply(lambda x: hash(x.wkt))
        c1 = old1 != new1
    else:
        c1 = old_set[parameter] != new_set[parameter]
    notnan1 = old_set[parameter].notnull() | new_set[parameter].notnull()
    c2 = c1 & notnan1

    if (len(comp1) == len(comp2)) and (~c2).all():
        all_set = pd.DataFrame()
    else:
        diff_set = new_set[c2].copy()
        old_set2 = old_set[~c2].copy()

        if add_old:
            not_cols = list(on)
            [not_cols.extend([c]) for c in comp1.columns if '_x' in c]
            add_old1 = comp1.loc[comp1._merge == 'left_only', not_cols].copy()
            add_old1.rename(columns=old_cols_map, inplace=True)

            all_set = pd.concat([old_set2, diff_set, add_set, add_old1])
        else:
            all_set = pd.concat([old_set2, diff_set, add_set])

    return all_set


def compare_xrs(old_xr, new_xr, add_old=False):
    """

    """
    ## Determine the parameter to be compared and the dimensions
    vars1 = list(new_xr.variables)
    parameter = [v for v in vars1 if 'dataset_id' in new_xr[v].attrs][0]
    vars2 = [parameter]

    ## Determine if there are ancillary variables to pull through
    new_attrs = new_xr[parameter].attrs.copy()

    if 'ancillary_variables' in new_attrs:
        av1 = new_attrs['ancillary_variables'].split(' ')
        vars2.extend(av1)

    if not parameter in old_xr:
        raise ValueError(parameter + ' must be in old_xr')

    ## Reduce the dimensions for the comparison for compatibility
    new1_s = new_xr[vars2].squeeze()
    on = list(new1_s.dims)

    # Fix for when there is no dimension > 1
    if len(on) == 0:
        new1_s = new1_s.expand_dims('time')
        on = ['time']

    old1_s = old_xr[vars2].squeeze()
    old_on = list(old1_s.dims)
    if len(old_on) == 0:
        old1_s = old1_s.expand_dims('time')
        old_on = ['time']

    if not on == old_on:
        raise ValueError('Dimensions are not the same between the datasets')

    ## Assign variables
    keep_vars = on + vars2

    new_all_vars = list(new1_s.variables)
    new_bad_vars = [v for v in new_all_vars if not v in keep_vars]
    new2_s = new1_s.drop(new_bad_vars)

    old_all_vars = list(old1_s.variables)
    old_bad_vars = [v for v in old_all_vars if not v in keep_vars]
    old2_s = old1_s.drop(old_bad_vars)

    # Fix datetime rounding issues...
    for v in list(old2_s.variables):
        if old2_s[v].dtype.name == 'datetime64[ns]':
            old2_s[v] = old2_s[v].dt.round('s')

    for v in list(new2_s.variables):
        if new2_s[v].dtype.name == 'datetime64[ns]':
            new2_s[v] = new2_s[v].dt.round('s')

    ## Pull out data for comparison
    old_df = old2_s.to_dataframe().reset_index()
    new_df = new2_s.to_dataframe().reset_index()

    ## run comparison
    comp = compare_dfs(old_df, new_df, on, parameter, add_old=add_old)

    if comp.empty:
        # print('Nothing has changed. Returning empty DataFrame.')
        return comp

    else:

        ## Repackage into netcdf
        comp2 = comp.set_index(list(on)).sort_index().to_xarray()

        # Fix datetime rounding issues...
        for v in list(comp2.variables):
            if comp2[v].dtype.name == 'datetime64[ns]':
                comp2[v] = comp2[v].dt.round('s')

        for v in vars1:
            if v not in vars2:
                if v not in on:
                    comp2[v] = new_xr[v].copy()
                comp2[v].attrs = new_xr[v].attrs.copy()
                comp2[v].encoding = new_xr[v].encoding.copy()

        new_dims = new_xr[parameter].dims
        dim_dict = dict(comp2.dims)
        data_shape = tuple(dim_dict[d] for d in new_dims)

        for v in vars2:
            comp2 = comp2.assign({v: (new_dims, comp2[v].values.reshape(data_shape))})
            comp2[v].attrs = new_xr[v].attrs.copy()
            comp2[v].encoding = new_xr[v].encoding.copy()

        comp2.attrs = new_xr.attrs.copy()
        comp2.encoding = new_xr.encoding.copy()

        return comp2


def assign_ds_ids(datasets):
    """
    Parameters
    ----------
    datasets : list
    """
    dss = copy.deepcopy(datasets)

    ### Iterate through the dataset list
    for ds in dss:
        # print(ds)
        ## Validate base model
        _ = DatasetBase(**ds)

        base_ds = {k: ds[k] for k in base_ds_fields}
        base_ds_b = orjson.dumps(base_ds, option=orjson.OPT_SERIALIZE_NUMPY)
        ds_id = blake2b(base_ds_b, digest_size=12).hexdigest()

        ds['dataset_id'] = ds_id

        ## Validate full model
        _ = Dataset(**ds)

    return dss


def process_datasets(datasets):
    """

    """
    if isinstance(datasets, dict):
        for ht_ds, ds_list in datasets.items():
            ds_list2 = assign_ds_ids(ds_list)
            datasets[ht_ds] = ds_list2

        dataset_list = []
        [dataset_list.extend(ds_list) for ht_ds, ds_list in datasets.items()]
    elif isinstance(datasets, list):
        dataset_list = assign_ds_ids(datasets)
    else:
        raise TypeError('datasets must be either a dict or list.')

    return dataset_list


def create_geometry_df(df, extent=False, altitude=True, to_wkb_hex=True, precision=7, check_geometries=True):
    """

    """
    if extent:
        if ('lon' in df) and ('lon' in df):
            min_lon = round(df['lon'].min(), precision)
            max_lon = round(df['lon'].max(), precision)
            min_lat = round(df['lat'].min(), precision)
            max_lat = round(df['lat'].max(), precision)
            geometry = pd.Series(box(min_lon, min_lat, max_lon, max_lat))
            # geometry = shape(geojson.Polygon([[(min_lon, min_lat), (min_lon, max_lat), (max_lon, max_lat), (max_lon, min_lat), (min_lon, min_lat)]], True, precision=precision))
        else:
            raise ValueError('Extent must have lat and lon in the df.')
    else:
        if 'geometry' in df:
            geometry = df['geometry']
        elif ('lon' in df) and ('lon' in df):
            if altitude:
                if 'altitude' in df:
                    coords = df.apply(lambda x: (round(x.lon, precision), round(x.lat, precision), x.altitude), axis=1)
                else:
                    coords = df.apply(lambda x: (round(x.lon, precision), round(x.lat, precision)), axis=1)
            else:
                coords = df.apply(lambda x: (round(x.lon, precision), round(x.lat, precision)), axis=1)
            geometry = coords.apply(lambda x: Point(x))
            # geometry = coords.apply(lambda x: shape(geojson.Point(x, True, precision=precision)))
        else:
            raise ValueError('Either a dict of geometry or a combo of lat and lon must be in the dataframe.')

        ## Check if geometries are valid (according to shapely)
        if check_geometries:
            for g in geometry:
                if not g.is_valid:
                    raise ValueError(str(g) + ': This shapely geometry is not valid')

        if to_wkb_hex:
            geometry = geometry.apply(lambda x: x.wkb_hex)

    return geometry


def assign_station_id(geometry):
    """
    Parameters
    ----------
    geoemtry : shapely geometry class
    """
    station_id = blake2b(geometry.wkb, digest_size=12).hexdigest()

    return station_id


def assign_station_ids_df(stns_df, extent=False, precision=5):
    """

    """
    geometry = create_geometry_df(stns_df, extent=extent, altitude=False, to_wkb_hex=False, precision=precision)

    stn_ids = geometry.apply(lambda x: assign_station_id(x))

    return stn_ids


# def process_stations_df(stns, dataset_id=None, remote=None):
#     """

#     """
#     ## Get existing stations from tethys
#     if isinstance(dataset_id, str) and isinstance(remote, dict):
#         try:
#             tethys = Tethys([remote])
#             remote_stns = tethys.get_stations(dataset_id)
#             remote_stns1 = pd.DataFrame(remote_stns)[['station_id', 'ref']]

#             ## Assign station_ids
#             stns2 = pd.merge(stns, remote_stns1, on='ref', how='left')
#         except:
#             stns2 = stns.copy()
#             stns2['station_id'] = np.nan
#     else:
#         stns2 = stns.copy()
#         stns2['station_id'] = np.nan

#     stns2.loc[stns2['station_id'].isnull(), 'station_id'] = assign_station_ids_df(stns2[stns2['station_id'].isnull()])
#     stns2 = stns2.drop_duplicates('station_id').copy()

#     ## Assign geometries
#     stns2['geometry'] = create_geometry_df(stns2, to_wkb_hex=True, precision=6)

#     ## Final station processing
#     stns3 = stns2.drop(['lat', 'lon'], axis=1)

#     return stns3


def process_sparse_stations_from_df(stns, dataset_id=None, connection_config=None, bucket=None, version=2):
    """
    Function that takes a stns dataframe of station data and converts it to an Xarray Dataset for Tethys. This is ultimately meant to be combined with the time series data for futher processing. If a geometry column is provided, it must be as a geojson-type dict (not a geopandas column).

    """
    ## Get existing stations from tethys
    if isinstance(dataset_id, str) and isinstance(connection_config, (dict, str)) and isinstance(bucket, str):
        try:
            remote = {'connection_config': connection_config, 'bucket': bucket, 'version': version}
            tethys = Tethys([remote])
            remote_stns = tethys.get_stations(dataset_id)
            remote_stns1 = pd.DataFrame(remote_stns)[['station_id', 'ref']]

            ## Assign station_ids
            stns2 = pd.merge(stns, remote_stns1, on='ref', how='left')
        except:
            stns2 = stns.copy()
            stns2['station_id'] = np.nan
    else:
        stns2 = stns.copy()
        stns2['station_id'] = np.nan

    stn_bool = stns2['station_id'].isnull()

    if any(stn_bool):
        stns2.loc[stns2['station_id'].isnull(), 'station_id'] = assign_station_ids_df(stns2[stns2['station_id'].isnull()])

    stns2 = stns2.drop_duplicates('station_id').copy()

    ## Assign geometries
    stns2['geometry'] = create_geometry_df(stns2, to_wkb_hex=True, precision=6)

    ## Final station processing
    stns3 = stns2.drop(['lat', 'lon'], axis=1).set_index('geometry')

    stns4 = stns3.to_xarray()

    return stns4


def stations_dict_to_df(stns):
    """

    """
    s1 = copy.deepcopy(stns)
    _ = [s.pop('stats') for s in s1]
    _ = [s.pop('virtual_station') for s in s1 if 'virtual_station' in s]
    _ = [s.pop('modified_date') for s in s1 if 'modified_date' in s]
    _ = [s.pop('dataset_id') for s in s1]

    ## Process attrs
    attrs = {}
    for s in s1:
        if 'properties' in s:
            if s['properties']:
                for pk, pv in s['properties'].items():
                    attrs.update({pk: pv['attrs']})
                    if isinstance(pv['data'], list):
                        s.update({pk: pv['data'][0]})
                    else:
                        s.update({pk: pv['data']})
            s.pop('properties')

    ## Convert to df
    s2 = pd.DataFrame(s1)

    ## Process geometry
    s2['geometry'] = create_geometry_df(s2, to_wkb_hex=True, precision=6)

    ## Return
    return s2, attrs


def prepare_new_xr(ts_data, stn_data, mod_date=True):
    """

    """
    if isinstance(stn_data, pd.Series):
        stn = stn_data.to_frame().T.set_index('geometry').to_xarray()
    elif isinstance(stn_data, pd.DataFrame):
        stn = stn_data.set_index('geometry').to_xarray()
    elif isinstance(stn_data, dict):
        stn = pd.DataFrame([stn_data]).set_index('geometry').to_xarray()

    obs2 = ts_data.copy()

    obs2['geometry'] = stn['geometry'].values[0]

    obs2.set_index(['geometry', 'height', 'time'], inplace=True)

    if mod_date:
        mod_date = pd.Timestamp.today(tz='utc').round('s').tz_localize(None)
        obs2['modified_date'] = mod_date

    obs3 = obs2.to_xarray()
    obs4 = xr.combine_by_coords([obs3, stn], data_vars='minimal')

    return obs4


def get_new_stats(data):
    """

    """
    vars1 = list(data.variables)
    parameter = [v for v in vars1 if 'dataset_id' in data[v].attrs][0]
    precision = int(np.abs(np.log10(data[parameter].attrs['precision'])))
    data1 = data[parameter]

    min1 = round(float(data1.min()), precision)
    max1 = round(float(data1.max()), precision)
    mean1 = round(float(data1.mean()), precision)
    median1 = round(float(data1.median()), precision)
    count1 = int(data1.count())

    stats1 = Stats(min=min1, max=max1, mean=mean1, median=median1, count=count1)

    return stats1


def get_station_data_from_xr(data):
    """
    Parameters
    ----------
    data : xr.Dataset
    """
    vars1 = list(data.variables)
    dims0 = dict(data.dims)
    dims1 = list(dims0.keys())
    parameter = [v for v in vars1 if 'dataset_id' in data[v].attrs][0]
    attrs = data[parameter].attrs.copy()
    data_vars = [parameter]
    if 'ancillary_variables' in attrs:
        ancillary_variables = attrs['ancillary_variables'].split(' ')
        data_vars.extend(ancillary_variables)

    stn_fields = list(StationBase.schema()['properties'].keys())

    ## Geometry
    if 'station_geometry' in dims1:
        geo1 = mapping(wkb.loads(data['station_geometry'].values[0], True))
    elif 'geometry' in dims1:
        geo1 = mapping(wkb.loads(data['geometry'].values[0], True))
    else:
        lon = data['lon'].values[0]
        lat = data['lat'].values[0]
        geo1 = geojson.Point([lon, lat], True, 7)

    stn_fields.remove('geometry')

    lat_lon = ['lon', 'lat']

    stn_vars = [v for v in vars1 if (not v in dims1) and (not v in data_vars) and (not v in lat_lon)]
    if ('geometry' in dims1) or ('station_geometry' in dims1):
        stn_data1 = {k: v['data'][0] for k, v in data[stn_vars].to_dict()['data_vars'].items() if k in stn_fields}
        props = {s: {'data': data[s].to_dict()['data'][0], 'attrs': data[s].to_dict()['attrs']} for s in stn_vars if s not in stn_fields}
    else:
        stn_data1 = {k: v['data'][0][0] for k, v in data[stn_vars].to_dict()['data_vars'].items() if k in stn_fields}
        props = {s: {'data': data[s].to_dict()['data'][0][0], 'attrs': data[s].to_dict()['attrs']} for s in stn_vars if s not in stn_fields}
    stn_data1.update({'geometry': geo1})
    if 'altitude' in stn_data1:
        stn_data1['altitude'] = round(stn_data1['altitude'], 3)
    # if not 'virtual_station' in stn_data1:
    #     stn_data1['virtual_station'] = False

    stn_data1['dimensions'] = dims0
    stn_data1['heights'] = data['height'].values.tolist()

    from_date = pd.Timestamp(data['time'].min().values).tz_localize(None)
    to_date = pd.Timestamp(data['time'].max().values).tz_localize(None)

    stn_data1['time_range'] = {'from_date': from_date, 'to_date': to_date}
    stn_data1['dataset_id'] = attrs['dataset_id']

    ## get the stats
    stats1 = get_new_stats(data)
    stn_data1['stats'] = stats1

    if props:
        stn_data1['properties'] = props

    ## Check model
    stn_m = StationBase(**stn_data1)

    return stn_m.dict(exclude_none=True)


def process_station_summ(data, object_infos, mod_date=None):
    """

    """
    if mod_date is None:
        mod_date = pd.Timestamp.today(tz='utc').round('s').tz_localize(None)
    elif isinstance(mod_date, (str, pd.Timestamp)):
        mod_date = pd.Timestamp(mod_date).tz_localize(None)

    ## Append the obj infos to the other station data
    stn_dict2 = get_station_data_from_xr(data)
    stn_dict2.update({'results_object_key': object_infos, 'modified_date': mod_date})

    station_m = Station(**stn_dict2)

    stn_dict = orjson.loads(station_m.json(exclude_none=True))

    return stn_dict


def prepare_results(data_dict, dataset_list, results_data, run_date_key, sum_closed='right', other_closed='left', discrete=True, other_attrs=None, other_encoding=None):
    """

    """
    tz_str = 'Etc/GMT{0:+}'

    parameter = dataset_list[0]['parameter']

    if parameter not in results_data:
        raise ValueError('The parameter ' + str(parameter) + ' is not in the results_data.')

    ## Determine index
    data_index = tuple(results_data.dims)
    vars2 = list(results_data.variables)
    vars3 = [v for v in vars2 if v not in data_index]

    vars_dict = {}
    for v in vars3:
        index1 = results_data[v].dims
        vars_dict[v] = index1

    ancillary_variables = [v for v, i in vars_dict.items() if (i == data_index) and (v != parameter)]

    main_vars = [parameter] + ancillary_variables

    if not 'time' in data_index:
        raise ValueError('time must be in the data_df index.')

    other_index = [i for i in data_index if i != 'time']

    ## Iterate through each dataset
    for ds in dataset_list:
        # print(ds['dataset_id'])

        ds_mapping = copy.deepcopy(ds)
        properties = ds_mapping.pop('properties')
        if 'attrs' in properties:
            attrs = properties['attrs']
        else:
            attrs = {}
        encoding = properties['encoding']

        attrs1 = copy.deepcopy(attrs)
        attrs1.update({ds_mapping['parameter']: ds_mapping})

        if isinstance(other_attrs, dict):
            attrs1.update(other_attrs)

        encoding1 = copy.deepcopy(encoding)

        if isinstance(other_encoding, dict):
            encoding1.update(other_encoding)

        ## Pre-Process data
        qual_col = 'quality_code'
        freq_code = ds_mapping['frequency_interval']
        utc_offset = ds_mapping['utc_offset']

        main_cols = list(data_index)
        main_cols.extend([parameter])

        ts_data1 = results_data.copy()

        # Convert times to local TZ if necessary
        if (not freq_code in ['T', 'H', '1H']) and (not utc_offset == '0H'):
            t1 = int(utc_offset.split('H')[0])
            tz1 = tz_str.format(-t1)
            ts_data1['time'] = ts_data1['time'].to_index().tz_localize('UTC').tz_convert(tz1).tz_localize(None)

        ## Aggregate data if necessary
        # Parameter
        if freq_code == 'T':
            data2 = ts_data1
        else:
            agg_fun = agg_stat_mapping[ds_mapping['aggregation_statistic']]

            ts_data2 = ts_data1[main_vars].to_dataframe()

            if agg_fun == 'sum':
                data0 = grp_ts_agg(ts_data2[parameter].reset_index(), other_index, 'time', freq_code, agg_fun, closed=sum_closed)
            else:
                data0 = grp_ts_agg(ts_data2[parameter].reset_index(), other_index, 'time', freq_code, agg_fun, discrete, closed=other_closed)

            # Ancillary variables
            av_list = [data0]
            for av in ancillary_variables:
                if qual_col == av:
                    ts_data2[qual_col] = pd.to_numeric(ts_data2[qual_col], errors='coerce', downcast='integer')
                    qual1 = grp_ts_agg(ts_data2[qual_col].reset_index(), other_index, 'time', freq_code, 'min')
                    av_list.append(qual1)
                else:
                    av1 = grp_ts_agg(ts_data2[av].reset_index(), other_index, 'time', freq_code, 'max')
                    av_list.append(av1)

            # Put the data together
            data1 = pd.concat(av_list, axis=1)
            data2 = data1.to_xarray()
            for v in vars3:
                if v not in data2:
                    data2[v] = ts_data1[v]

            del ts_data2
            del data1

        # Convert time back to UTC if necessary
        if (not freq_code in ['T', 'H', '1H']) and (not utc_offset == '0H'):
            data2['time'] = data2['time'].to_index().tz_localize(tz1).tz_convert('utc').tz_localize(None)

        ## Check if the entire record is nan
        n_data = int(data2[parameter].notnull().sum())

        if n_data > 0:

            ## Package up the netcdf object
            new1 = package_xarray(data2, parameter, attrs1, encoding1, run_date=run_date_key, compression='zstd')

            ## Update the data_dict
            ds_id = ds_mapping['dataset_id']

            if isinstance(data_dict, dict):
                data_dict[ds_id].append(new1)
            elif isinstance(data_dict, list):
                data_dict.append({ds_id: new1})
            else:
                raise TypeError('data_dict must be a dict or a list.')

        del ts_data1
        del data2


def prepare_results_v02(dataset, results_data, run_date_key, sum_closed='right', other_closed='left', discrete=True, other_attrs=None, other_encoding=None, skip_resampling=False):
    """

    """
    tz_str = 'Etc/GMT{0:+}'

    parameter = dataset['parameter']

    if parameter not in results_data:
        raise ValueError('The parameter ' + str(parameter) + ' is not in the results_data.')

    ## Determine index
    data_index = tuple(results_data.dims)
    vars2 = list(results_data.variables)
    vars3 = [v for v in vars2 if v not in data_index]

    vars_dict = {}
    for v in vars3:
        index1 = results_data[v].dims
        vars_dict[v] = index1

    ancillary_variables = [v for v, i in vars_dict.items() if (i == data_index) and (v != parameter)]

    main_vars = [parameter] + ancillary_variables

    if not 'time' in data_index:
        raise ValueError('time must be in the data_df index.')

    other_index = [i for i in data_index if i != 'time']

    ## Iterate through each dataset
    ds_mapping = copy.deepcopy(dataset)
    properties = ds_mapping.pop('properties')
    if 'attrs' in properties:
        attrs = properties['attrs']
    else:
        attrs = {}
    encoding = properties['encoding']

    attrs1 = copy.deepcopy(attrs)
    attrs1.update({ds_mapping['parameter']: ds_mapping})

    if isinstance(other_attrs, dict):
        attrs1.update(other_attrs)

    encoding1 = copy.deepcopy(encoding)

    if isinstance(other_encoding, dict):
        encoding1.update(other_encoding)

    ## Pre-Process data
    qual_col = 'quality_code'
    freq_code = ds_mapping['frequency_interval']
    utc_offset = ds_mapping['utc_offset']

    main_cols = list(data_index)
    main_cols.extend([parameter])

    ts_data1 = results_data

    # Convert times to local TZ if necessary
    if (not freq_code in ['T', 'H', '1H']) and (not utc_offset == '0H'):
        t1 = int(utc_offset.split('H')[0])
        tz1 = tz_str.format(-t1)
        ts_data1['time'] = ts_data1['time'].to_index().tz_localize('UTC').tz_convert(tz1).tz_localize(None)

    ## Aggregate data if necessary
    # Parameter
    if (freq_code == 'T') or skip_resampling:
        data2 = ts_data1
    else:
        agg_fun = agg_stat_mapping[ds_mapping['aggregation_statistic']]

        ts_data2 = ts_data1[main_vars].to_dataframe()

        if agg_fun == 'sum':
            data0 = grp_ts_agg(ts_data2[parameter].reset_index(), other_index, 'time', freq_code, agg_fun, closed=sum_closed)
        else:
            data0 = grp_ts_agg(ts_data2[parameter].reset_index(), other_index, 'time', freq_code, agg_fun, discrete, closed=other_closed)

        # Ancillary variables
        av_list = [data0]
        for av in ancillary_variables:
            if qual_col == av:
                ts_data2[qual_col] = pd.to_numeric(ts_data2[qual_col], errors='coerce', downcast='integer')
                qual1 = grp_ts_agg(ts_data2[qual_col].reset_index(), other_index, 'time', freq_code, 'min')
                av_list.append(qual1)
            else:
                av1 = grp_ts_agg(ts_data2[av].reset_index(), other_index, 'time', freq_code, 'max')
                av_list.append(av1)

        # Put the data together
        data1 = pd.concat(av_list, axis=1)
        data2 = data1.to_xarray()
        for v in vars3:
            if v not in data2:
                data2[v] = ts_data1[v]

        del ts_data2
        del data1

    # Convert time back to UTC if necessary
    if (not freq_code in ['T', 'H', '1H']) and (not utc_offset == '0H'):
        data2['time'] = data2['time'].to_index().tz_localize(tz1).tz_convert('utc').tz_localize(None)

    ## Check if the entire record is nan
    n_data = int(data2[parameter].notnull().sum())

    del ts_data1

    if n_data > 0:

        ## Package up the netcdf object
        new1 = package_xarray(data2, parameter, attrs1, encoding1, run_date=run_date_key, compression='zstd')

        del data2

        ## Update the data_dict
        # ds_id = ds_mapping['dataset_id']

        return new1

    else:
        return None


def stats_for_dataset_metadata(stns):
    """
    I need time_range, extent, and if grid the spatial_resolution.
    """
    dict1 = {}
    ## spatial resolution
    if 'lat' in stns[0]['dimensions']:
        lat_dim = int(np.median([s['dimensions']['lat'] for s in stns]))

        type1 = stns[0]['geometry']['type']

        if type1 in ['Polygon', 'Line']:
            geo = [s['geometry']['coordinates'][0][0][-1] for s in stns]
        else:
            geo = [s['geometry']['coordinates'][-1] for s in stns]

        geo1 = np.array(geo).round(5)
        geo1.sort()
        diff1 = np.diff(geo1)
        res1 = round(np.median(diff1[diff1 > 0])/lat_dim, 5)

        dict1.update({'spatial_resolution': res1})

    ## Extent
    geo = np.array([s['geometry']['coordinates'] for s in stns]).round(5)

    len1 = int(np.prod(geo.shape)/2)
    geo1 = geo.T.reshape(2, len1)
    min_lon, min_lat = geo1.min(axis=1)
    max_lon, max_lat = geo1.max(axis=1)

    extent1 = mapping(box(min_lon, min_lat, max_lon, max_lat))

    dict1.update({'extent': extent1})

    ## time range
    trange1 = np.array([[s['time_range']['from_date'], s['time_range']['to_date']] for s in stns])
    mins, maxes = trange1.T

    min_t = min(mins)
    max_t = max(maxes)

    dict1.update({'time_range': {'from_date': min_t, 'to_date': max_t}})

    ## Heights
    heights1 = []
    [heights1.extend(s['heights']) for s in stns]
    heights2 = list(set(heights1))
    heights2.sort()

    dict1.update({'heights': heights2})

    return dict1
















