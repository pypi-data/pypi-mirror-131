"""
Created on 2020-11-05.

@author: Mike K
"""
import os
import requests
import numpy as np
import xarray as xr
import pandas as pd
import orjson
# import yaml
from datetime import datetime
import copy
from multiprocessing.pool import ThreadPool
from tethysts.utils import get_object_s3, result_filters, process_results_output, read_json_zstd, key_patterns, get_nearest_station, get_intersected_stations, spatial_query, convert_results_v2_to_v3, get_nearest_from_extent, read_pkl_zstd, public_remote_key, convert_results_v3_to_v4
# from utils import get_object_s3, result_filters, process_results_output, read_json_zstd, key_patterns, get_nearest_station, get_intersected_stations, spatial_query, convert_results_v2_to_v3, get_nearest_from_extent, read_pkl_zstd, public_remote_key, convert_results_v3_to_v4
from typing import Optional, List, Any, Union
from enum import Enum
import tethys_data_models as tdm

pd.options.display.max_columns = 10


##############################################
### data models



##############################################
### Class


class Tethys(object):
    """
    The base Tethys object.

    Parameters
    ----------
    remotes : list of dict or None
        list of dict of the S3 remotes to access or None which will parse all public datasets.
        The dicts must contain:
        bucket and connection_config.

        bucket : str
            A string of the bucket name.
        connection_config : dict or str
            A dict of strings of service_name, s3, endpoint_url, aws_access_key_id, and aws_secret_access_key. Or it could be a string of the public_url endpoint.

    Returns
    -------
    tethys object
    """
    ## Initial import and assignment function
    def __init__(self, remotes=None):
        """

        """
        setattr(self, 'datasets', [])
        setattr(self, '_datasets', {})
        setattr(self, '_remotes', {})
        setattr(self, '_stations', {})
        setattr(self, '_key_patterns', key_patterns)
        setattr(self, '_results', {})
        setattr(self, '_results_obj_keys', {})

        if isinstance(remotes, list):
            _ = self.get_datasets(remotes)

        elif remotes is None:
            resp = requests.get(public_remote_key)
            resp.raise_for_status()

            remotes = read_json_zstd(resp.content)
            _ = self.get_datasets(remotes)

        elif remotes != 'pass':
            raise ValueError('remotes must be a list of dict or None.')

        pass


    def get_datasets(self, remotes: List[dict], threads: int = 30):
        """
        The function to get datasets from many remotes.

        Parameters
        ----------
        remotes : list of dict
            list of dict of the S3 remotes to access. The dicts must contain:
            bucket and connection_config.
            bucket : str
                A string of the bucket name.
            connection_config : dict or str
                A dict of strings of service_name, s3, endpoint_url, aws_access_key_id, and aws_secret_access_key. Or it could be a string of the public_url endpoint.
        threads : int
            The number of threads to use. I.e. the number of simultaneous remote reads.

        Returns
        -------
        dict
            of datasets
        """
        ## Validate remotes
        for remote in remotes:
            _ = tdm.base.Remote(**remote)

        _ = ThreadPool(threads).map(self.get_remote_datasets, remotes)
        setattr(self, 'remotes', remotes)

        return self.datasets


    def get_remote_datasets(self, remote: dict):
        """
        Get datasets from an individual remote. Saves result into the object.

        Parameters
        ----------
        remote : dict
            dict of the S3 remote to access. The dict must contain:
            bucket and connection_config.
            bucket : str
                A string of the bucket name.
            connection_config : dict or str
                A dict of strings of service_name, s3, endpoint_url, aws_access_key_id, and aws_secret_access_key. Or it could be a string of the public_url endpoint.
            version: int
                The S3 object structure version.

        Returns
        -------
        None
        """
        if 'version' in remote:
            version = remote['version']
        else:
            version = 2

        try:
            ds_obj = get_object_s3(self._key_patterns[version]['datasets'], remote['connection_config'], remote['bucket'])
            ds_list = read_json_zstd(ds_obj)

            ds_list2 = copy.deepcopy(ds_list)
            # [l.pop('properties') for l in ds_list2]
            self.datasets.extend(ds_list2)

            ds_dict = {d['dataset_id']: d for d in ds_list}
            remote_dict = {d: {'dataset_id': d, 'bucket': remote['bucket'], 'connection_config': remote['connection_config'], 'version': version} for d in ds_dict}

            self._datasets.update(ds_dict)
            self._remotes.update(remote_dict)

        except:
            print('No datasets.json.zst file in S3 bucket')


    def get_stations(self,
                     dataset_id: str,
                     geometry: Optional[dict] = None,
                     lat: Optional[float] = None,
                     lon: Optional[float] = None,
                     distance: Optional[float] = None,
                     results_object_keys: Optional[bool] = False):
        """
        Method to return the stations associated with a dataset.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.
        geometry : dict or None
            A geometry in GeoJSON format. Can be either a point or a polygon. If it's a point, then the method will perform a nearest neighbor query and return one station. If it's a polygon, then the method performs an intersection of all stations within the polygon.
        lat : float or None
            Instead of using the geometry parameter, optionally use lat and lon for the spatial queries. Both lat and lon must be passed for the spatial queries and will override the geometry parameter. If only lat and lon are passed, then the method performs a nearest neighbor query. If distance is passed in addition to lat and lon, then distance is used as a radius buffer and an intersection is performed.
        lon : float or None
            See lat description.
        distance : float or None
            See lat description. This should be in decimal degrees not meters.
        results_object_keys : bool
            Shoud the results object keys be returned? The results object keys list the available results in Tethys.

        Returns
        -------
        list of dict
            of station data
        """
        remote = self._remotes[dataset_id]

        site_key = self._key_patterns[remote['version']]['stations'].format(dataset_id=dataset_id)

        if dataset_id in self._stations:
            stn_dict = copy.deepcopy(self._stations[dataset_id])
        else:
            try:
                stn_obj = get_object_s3(site_key, remote['connection_config'], remote['bucket'])
                stn_list = read_json_zstd(stn_obj)
                stn_dict = {s['station_id']: s for s in stn_list if isinstance(s, dict)}
            except:
                print('No stations.json.zst file in S3 bucket')
                return None

            ## Results obj keys if old version
            if not 'version' in self._datasets[dataset_id]:

                res_obj_keys = {si: s['results_object_key'] for si, s in stn_dict.items()}
                self._results_obj_keys.update({dataset_id: copy.deepcopy(res_obj_keys)})
                [s.update({'results_object_key': s['results_object_key'][-1]}) for i, s in stn_dict.items()]

            self._stations.update({dataset_id: copy.deepcopy(stn_dict)})

        ## Spatial query
        stn_ids = spatial_query(stn_dict, geometry, lat, lon, distance)

        if isinstance(stn_ids, list):
            stn_list1 = [stn_dict[s] for s in stn_ids]
        else:
            stn_list1 = list(stn_dict.values())

        if not results_object_keys:
            [s.pop('results_object_key') for s in stn_list1]

        return stn_list1


    def _get_obj_keys(self, dataset_id: str):
        """

        """
        if dataset_id in self._results_obj_keys:
            obj_keys = self._results_obj_keys[dataset_id]
        else:
            if 'version' in self._datasets[dataset_id]:
                remote = self._remotes[dataset_id]

                ro_key = self._key_patterns[remote['version']]['results_object_keys'].format(dataset_id=dataset_id)
                ro_obj = get_object_s3(ro_key, remote['connection_config'], remote['bucket'])
                ro_list = read_json_zstd(ro_obj)

                obj_keys = {s['station_id']: s['results_object_key'] for s in ro_list}
                self._results_obj_keys.update({dataset_id: copy.deepcopy(obj_keys)})
            else:
                _ = self.get_stations(dataset_id)
                obj_keys = self._results_obj_keys[dataset_id]

        return obj_keys


    def get_run_dates(self, dataset_id: str, station_id: str):
        """
        Function to get the run dates of a particular dataset and station.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.
        station_id : str
            The station_id of the associated station.

        Returns
        -------
        list
        """
        res_obj_keys = self._get_obj_keys(dataset_id)

        obj_keys = res_obj_keys[station_id]

        run_dates = np.unique([ob['run_date'].split('+')[0] if '+' in ob['run_date'] else ob['run_date'] for ob in obj_keys]).tolist()

        return run_dates


    def _get_results_obj_key_s3(self, dataset_id: str, station_id: str, run_date: Union[str, pd.Timestamp]):
        """

        """
        if isinstance(run_date, (str, pd.Timestamp)):
            res_obj_keys = self._get_obj_keys(dataset_id)

            obj_keys = res_obj_keys[station_id]

            obj_keys_df = pd.DataFrame(obj_keys)
            obj_keys_df['run_date'] = pd.to_datetime(obj_keys_df['run_date']).dt.tz_localize(None)

            run_date1 = pd.Timestamp(run_date)

            obj_key_df = obj_keys_df[obj_keys_df['run_date'] == run_date1]

            if obj_key_df.empty:
                raise ValueError('Requested run_date is not available, run the get_run_dates method.')
            else:
                obj_key = obj_key_df['key'].iloc[0]

        else:
            if dataset_id not in self._stations:
                _ = self.get_stations(dataset_id)

            stn = self._stations[dataset_id][station_id]

            obj_key = stn['results_object_key']['key']

        return obj_key


    def get_results(self,
                    dataset_id: str,
                    station_id: Optional[str] = None,
                    geometry: Optional[dict] = None,
                    lat: Optional[float] = None,
                    lon: Optional[float] = None,
                    from_date: Union[str, pd.Timestamp, datetime, None] = None,
                    to_date: Union[str, pd.Timestamp, datetime, None] = None,
                    from_mod_date: Union[str, pd.Timestamp, datetime, None] = None,
                    to_mod_date: Union[str, pd.Timestamp, datetime, None] = None,
                    modified_date: Union[str, pd.Timestamp, datetime, None] = None,
                    quality_code: Optional[bool] = False,
                    run_date: Union[str, pd.Timestamp, datetime, None] = None,
                    squeeze_dims: Optional[bool] = False,
                    output: str = 'Dataset',
                    cache: Optional[str] = None):
        """
        Function to query the time series data given a specific dataset_id and station_id. Multiple optional outputs.

        Parameters
        ----------
        dataset_id : str
            The dataset_id of the dataset.
        station_id : str or None
            The station_id of the associated station.
        geometry : dict or None
            A geometry in GeoJSON format. Can be either a point or a polygon. If it's a point, then the method will perform a nearest neighbor query and return one station.
        lat : float or None
            Instead of using the geometry parameter, optionally use lat and lon for the spatial queries. Both lat and lon must be passed for the spatial queries and will override the geometry parameter. If only lat and lon are passed, then the method performs a nearest neighbor query.
        lon : float or None
            See lat description.
        from_date : str, Timestamp, datetime, or None
            The start date of the selection.
        to_date : str, Timestamp, datetime, or None
            The end date of the selection.
        from_mod_date : str, Timestamp, datetime, or None
            Only return data post the defined modified date.
        to_mod_date : str, Timestamp, datetime, or None
            Only return data prior to the defined modified date.
        modified_date : bool
            Should the modified dates be returned if they exist?
        quality_code : bool
            Should the quality codes be returned if they exist?
        run_date : str or Timestamp
            The run_date of the results to be returned. Defaults to None which will return the last run date.
        squeeze_dims : bool
            Should all dimensions with a length of one be removed from the parameter's dimensions?
        output : str
            Output format of the results. Options are:
                Dataset - return the entire contents of the netcdf file as an xarray Dataset,
                DataArray - return the requested dataset parameter as an xarray DataArray,
                Dict - return a dictionary of results from the DataArray,
                json - return a json str of the Dict.
        cache : str or None
            How the results should be cached. Current options are None (which does not cache) and 'memory' (which caches the results in the Tethys object in memory).

        Returns
        -------
        Whatever the output was set to.
        """

        ## Get parameters
        dataset = self._datasets[dataset_id]
        parameter = dataset['parameter']
        remote = self._remotes[dataset_id]

        if isinstance(geometry, dict):
            geom_type = geometry['type']
        else:
            geom_type = None

        if isinstance(station_id, str):
            stn_id = station_id
        elif ((geom_type in ['Point', 'Polygon']) or (isinstance(lat, float) and isinstance(lon, float))):
            ## Get all stations
            if dataset_id not in self._stations:
                _ = self.get_stations(dataset_id)

            stn_dict = self._stations[dataset_id]

            # Run the spatial query
            stn_id = spatial_query(stn_dict, geometry, lat, lon)[0]
        else:
            raise ValueError('A station_id, geometry or a combination of lat and lon must be passed.')

        ## Get object key
        obj_key = self._get_results_obj_key_s3(dataset_id, stn_id, run_date)

        ## Get results
        if obj_key in self._results:
            ts_obj = self._results[obj_key]
        else:
            ts_obj = get_object_s3(obj_key, remote['connection_config'], remote['bucket'])

        # cache results if requested
        if cache == 'memory':
            if obj_key in self._results:
                new_len = len(ts_obj)
                old_len = len(self._results[obj_key])
                if new_len != old_len:
                    self._results[obj_key] = ts_obj
            else:
                self._results[obj_key] = ts_obj

        # Open results
        xr3 = xr.open_dataset(read_pkl_zstd(ts_obj))

        ## Convert to new version
        attrs = xr3.attrs.copy()
        if ('version' not in attrs):
            xr3 = convert_results_v2_to_v3(xr3)
            attrs['version'] = 3

        if attrs['version'] == 3:
            xr3 = convert_results_v3_to_v4(xr3)

        ## Extra spatial query if data are stored in blocks
        if ('station_geometry' in xr3) and ((geom_type == 'Point') or (isinstance(lat, float) and isinstance(lon, float))):
            xr3 = get_nearest_from_extent(xr3, geometry, lat, lon)

        ## Filters
        ts_xr1 = result_filters(xr3, from_date, to_date, from_mod_date, to_mod_date)

        # if not 'station_id' in list(ts_xr1.coords):
        #     ts_xr1 = ts_xr1.expand_dims('station_id').set_coords('station_id')

        ## Output
        output1 = process_results_output(ts_xr1, parameter, modified_date, quality_code, output, squeeze_dims)

        return output1


    def get_bulk_results(self,
                         dataset_id: str,
                         station_ids: List[str],
                         geometry: Optional[dict] = None,
                         lat: Optional[float] = None,
                         lon: Optional[float] = None,
                         from_date: Union[str, pd.Timestamp, datetime, None] = None,
                         to_date: Union[str, pd.Timestamp, datetime, None] = None,
                         from_mod_date: Union[str, pd.Timestamp, datetime, None] = None,
                         to_mod_date: Union[str, pd.Timestamp, datetime, None] = None,
                         modified_date: Optional[bool] = False,
                         quality_code: Optional[bool] = False,
                         run_date: Union[str, pd.Timestamp, datetime, None] = None,
                         squeeze_dims: Optional[bool] = False,
                         output: str = 'Dataset',
                         cache: Optional[str] = None,
                         threads: int = 30):
        """
        Function to bulk query the time series data given a specific dataset_id and a list of station_ids. The output will be specified by the output parameter and will be concatenated along the station_id dimension.

        Parameters
        ----------
        dataset_id : str
            The hashed str of the dataset_id.
        station_ids : list of str
            A list of hashed str of the site_ids.
        geometry : dict or None
            A geometry in GeoJSON format. Can be either a point or a polygon. If it's a point, then the method will perform a nearest neighbor query and return one station.
        lat : float or None
            Instead of using the geometry parameter, optionally use lat and lon for the spatial queries. Both lat and lon must be passed for the spatial queries and will override the geometry parameter. If only lat and lon are passed, then the method performs a nearest neighbor query.
        lon : float or None
            See lat description.
        from_date : str, Timestamp, datetime, or None
            The start date of the selection.
        to_date : str, Timestamp, datetime, or None
            The end date of the selection.
        from_mod_date : str, Timestamp, datetime, or None
            Only return data post the defined modified date.
        to_mod_date : str, Timestamp, datetime, or None
            Only return data prior to the defined modified date.
        modified_date : bool
            Should the modified dates be returned if they exist?
        quality_code : bool
            Should the quality codes be returned if they exist?
        run_date : str or Timestamp
            The run_date of the results to be returned. Defaults to None which will return the last run date.
        squeeze_dims : bool
            Should all dimensions with a length of one be removed from the parameter's dimensions?
        output : str
            Output format of the results. Options are:
                Dataset - return the entire contents of the netcdf file as an xarray Dataset,
                DataArray - return the requested dataset parameter as an xarray DataArray,
                Dict - return a dictionary of results from the DataArray,
                json - return a json str of the Dict.
        cache : str or None
            How the results should be cached. Current options are None (which does not cache) and 'memory' (which caches the results in the Tethys object in memory).
        threads : int
            The number of simultaneous downloads.

        Returns
        -------
        Format specified by the output parameter
            Will be concatenated along the station_id dimension
        """
        dataset = self._datasets[dataset_id]
        parameter = dataset['parameter']

        lister = [(dataset_id, s, geometry, lat, lon, from_date, to_date, from_mod_date, to_mod_date, modified_date, quality_code, run_date, False, 'Dataset', cache) for s in station_ids]

        output1 = ThreadPool(threads).starmap(self.get_results, lister)
        # output2 = [d if 'station_id' in list(d.coords) else d.expand_dims('station_id').set_coords('station_id') for d in output1]

        if 'geometry' in output1[0]:
            # deal with the situation where the variable names are not the same for all datasets
            try:
                xr_ds1 = xr.combine_nested(output1, 'geometry', data_vars='minimal', combine_attrs="override")
            except:
                xr_ds1 = xr.merge(output1, combine_attrs="override")
        else:
            try:
                xr_ds1 = xr.combine_by_coords(output1, data_vars='minimal')
            except:
                xr_ds1 = xr.merge(output1, combine_attrs="override")

        ## Output
        output3 = process_results_output(xr_ds1, parameter, modified_date, quality_code, output, squeeze_dims)

        return output3



######################################
### Testing
