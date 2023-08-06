from enum import Enum, unique # create user defined enumerations
import pandas as pd

@unique
class ActionType(Enum):
    ARTWORKS = 'artworks'
    AGENTS = 'agents'
    GALLERIES = 'galleries'
    EXHIBITIONS = 'exhibitions'
    CATALOGUES = 'catalogues'
    
    # get string version of enumeration from it's value
    def __str__(self):
        """
        Returns a string representation of this enumeration
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ActionType
        >>> a = ActionType.ARTWORKS
        >>> print('Selected type: {}'.format(str(a)))
        >>> Selected type: artworks
        """
        return self.value

# https://www.artic.edu/open-access/public-api
# https://api.artic.edu/docs/#introduction

class ArtInstChicagoApiClient(object):
    def __init__(self, use_internal_cache:bool = True):
        """
        Constructor.

        Parameters
        ----------
        use_internal_cache: bool, optional
            if true then store artworks, artists, galleries, exhibitions and catalogues 
            in an internal cache. Default value is True.

        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        """
        self.__base_url = 'https://api.artic.edu/api/v1'
        self.__limit = 100
        
        self.__use_internal_cache = use_internal_cache
        self.__clear_artworks_cache = False
        self.__clear_agents_cache = False
        self.__clear_galleries_cache = False
        self.__clear_exhibitions_cache = False
        self.__clear_catalogues_cache = False
        
        self.__artworks_cache = None
        self.__agents_cache = None
        self.__galleries_cache = None
        self.__exhibitions_cache = None
        self.__catalogues_cache = None
        self.__show_diagnostics = False
        
    # -----------------------
    # PROPERTIES
    # -----------------------
    @property
    def use_internal_cache(self) -> bool:
        """
        Get property for use_internal_cache
        
        Returns
        -------
        bool
            True to support and use an internal cache, False otherwise.
            
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient()
        >>> art_api_client.use_internal_cache = True
        >>> print('Use internal cache: {}'.format(art_api_client.use_internal_cache))
        """
        return self.__use_internal_cache
    
    @use_internal_cache.setter
    def use_internal_cache(self, use_cache:bool):
        """
        Set property for use_internal_cache
        
        Parameters
        ----------
        use_cache: bool
            True to support and use an internal cache, False otherwise.
            
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient()
        >>> art_api_client.use_internal_cache = True
        >>> print('Use internal cache: {}'.format(art_api_client.use_internal_cache))
        """
        self.__use_internal_cache = use_cache
        
    # -----------------------------------------------------------
    # UTILITY METHODS
    # -----------------------------------------------------------
    def __get_base_api_params(self) -> dict:
        """
        Utility method intended for internal use. Gets Dictionary of properties needed
        for querying public API for The Art Institute of Chicago. Contains 'page'
        and 'limit' properties at minimum.
        
        Returns
        -------
        dict
            Dictionary of properties needed for querying public API for
            The Art Institute of Chicago. Contains 'page' and 'limit'
            properties at minimum.
        """
        api_params = {'page': 1, 'limit': self.__limit}
        return api_params
    
    def __get_action_url(self, action:ActionType) -> str:
        """
        Utility method intended for internal use. Creates the appropriate
        url to invite the RESTful public API for The Art Institute of Chicago
        to retrieve certain type of data.
        
        Parameters
        ----------
        action: ActionType
            Identifies which action type to apply to the public API for
            The Art Institute of Chicago.
            
        Returns
        -------
        str
            The updated url to invite the RESTful public API for The Art
            Institute of Chicago to retrieve certain type of data.
        """
        assert isinstance(action, ActionType), "Invalid type for action"
        return '{0}/{1}'.format(self.__base_url, str(action))
    
    def __update_cache(self, cache:dict, results_lst:[], current_page:int, total_pages:int, total:int):
        """
        Utility method intended for internal use. Updates the internal data cache
        with results from API calls to prevent making redundant subsequent calls
        to the public API for The Art Institute of Chicago for the same data.
        
        Parameters
        ----------
        cache: dict
            The internal cache of a specific type of query features (e.g., cache for artworks).
        results_lst: list
            A list of the return json from a call to the public API for The Art
            Institute of Chicago to retrieve data. Each element of the list is the
            json of a different API call.
        current_page: int
            Indicates the max page of data stored for a multi-page set of json results.
        total_pages: int
            Indicates the total number of pages to get all of the data back for
            the intended query.
        total: int
            Indicates the total number of records for all of the data from
            the intended query.
        """
        cache['results_lst'] = results_lst
        cache['current_page'] = current_page
        cache['total_pages'] = total_pages
        cache['total'] = total
    
    def __print_diag_json(self, json_obj:object, indent:int = 4):
        """
        Utility method intended for internal use.
        
        Parameters
        ----------
        json_obj: object
            The json to be printed to the display console.
        indent: int, optional
            The number of spaces used in the indentation to properly
            format the json printed to the display console.
        """
        import json
        print(json.dumps(json_obj, indent = indent))

    def __get_pagination_info(self, request_json:object) -> (int, int, int):
        """
        Utility method intended for internal use. Gets the pagination details
        from the return json of the RESTful API call.
        
        Parameters
        ----------
        request_json: object
            The json from a call to the public API for The Art
            Institute of Chicago to retrieve data.
            
        Returns
        -------
        tuple
            Tuple of three integers representing the 'current page', 'total number of pages'
            and the 'total number of records'.
        """
        current_page, total_pages, total = 0, 0, 0
        
        if not request_json is None and 'pagination' in request_json:
            page_dict = request_json['pagination']
            current_page, total_pages, total = page_dict['current_page'], page_dict['total_pages'], page_dict['total']
            
        return current_page, total_pages, total
        
    def __get_request(self, target_url:str, api_params:dict, max_retries:int = 3) -> (int, object, str):
        """
        Utility method intended for internal use. Makes a call to a RESTful API, with
        the capability of retrying the attempt, and returns data returned from the API.
        
        Parameters
        ----------
        target_url: str
            The URL to the public API to invoke a specific remote query/action
            for data.
        api_params: dict
            The parameters to pass to the remote query/action.
        max_retries: int
            The maximum number of retry attempts to make if remote calls fail.
            
        Returns
        -------
        tuple
            Tuple of size three representing the HTTP status code of making a
            RESTful API call, the returned json data and the error message of
            an unexpected (but caught) exception.
        """
        import requests
        from requests.exceptions import HTTPError
        
        status_code = None
        result = None
        err_message = None
        
        re_run = True
        
        while re_run:
            try:
                req = requests.get(target_url, params = api_params)
                if not req is None:
                    status_code = req.status_code
                    # r.headers['content-type']
                    result = req.json()
                    re_run = False
                else:
                    status_code = 0
                    err_message = 'Missing or invalid returned request object'
                    re_run = False
            except HTTPError as http_err:
                status_code = 0
                err_message = 'HTTP Error: {0}'.format(http_err)
                max_retries -= 1
                re_run = True if max_retries >= 0 else False
            except Exception as err:
                status_code = 0
                err_message = 'Exception: {0}'.format(err)
                max_retries -= 1
                re_run = True if max_retries >= 0 else False
            
        return status_code, result, err_message
    
    def __get_json_as_dataframe(self, results_json_lst:[], parent_key:str, fields:[str]) -> pd.DataFrame:
        """
        Utility method intended for internal use. Transforms the json from the public
        RESTful API into a pandas DataFrame.
        
        Parameters
        ----------
        results_json_lst: list
            The URL to the public API to invoke a specific remote query/action
            for data.
        parent_key: str
            Key of portion of json to extract data from.
        fields: list
            List of data elements to retain from extracted json data.
            
        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the transformed json results from the
            RESTful API.
        """
        import pandas as pd
        data_df = None
        if not results_json_lst is None:
            count = len(results_json_lst)
            if count > 0:
                data_df = pd.DataFrame(data = results_json_lst[0][parent_key], columns = fields)
                for i in range(1, count):
                    data_df = data_df.append(pd.DataFrame(data = results_json_lst[i][parent_key], columns = fields), ignore_index = True)
                    
        return data_df
    
    def __get_data_and_pagination(self, action:ActionType, max_pages:int = 3) -> (list, list, list, int, int, int):
        """
        Utility method intended for internal use.
        """
        import numpy as np
        
        status_code_lst, results_lst, err_message_lst = [], [], []
        
        target_url = self.__get_action_url(action)
        api_params = self.__get_base_api_params()
        
        status_code, result, err_message = self.__get_request(target_url, api_params)
        current_page, total_pages, total = self.__get_pagination_info(result)
        
        if self.__show_diagnostics:
            self.__print_diag_json(result)
        
        status_code_lst.append(status_code)
        results_lst.append(result)
        err_message_lst.append(err_message)
        
        page_count = np.min([total_pages, max_pages])
        for i in range(current_page + 1, page_count + 1):
            api_params['page'] = i
            status_code, result, err_message = self.__get_request(target_url, api_params)
            current_page, _, _ = self.__get_pagination_info(result)
            
            if self.__show_diagnostics:
                self.__print_diag_json(result)
            
            status_code_lst.append(status_code)
            results_lst.append(result)
            err_message_lst.append(err_message)
            
        return status_code_lst, results_lst, err_message_lst, current_page, total_pages, total
        
    def __get_data(self, cache, clear_cache, action:ActionType, fields:[str]) -> (dict, bool, pd.DataFrame, int, int, int):
        """
        Utility method intended for internal use.
        """
        data_df, current_page, total_pages, total = None, None, None, None
        
        if cache is None or (not self.__use_internal_cache) or clear_cache:
            cache = {}
            status_code_lst, results_lst, err_message_lst, current_page, total_pages, total = self.__get_data_and_pagination(action)
            data_df = self.__get_json_as_dataframe(
                results_json_lst = results_lst,
                parent_key = 'data',
                fields = fields
            )
            self.__update_cache(cache, results_lst, current_page, total_pages, total)
            clear_cache = False
        else:
            current_page, total_pages, total = cache['current_page'], cache['total_pages'], cache['total']
            data_df = self.__get_json_as_dataframe(
                results_json_lst = cache['results_lst'],
                parent_key = 'data',
                fields = fields
            )
        
        return cache, clear_cache, data_df, current_page, total_pages, total
        
    # -----------------------------------------------------------
    # METHODS
    # -----------------------------------------------------------
    def clear_caches(self):
        """
        Empties the internal cache of data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> art_api_client.clear_caches()
        """
        if self.__use_internal_cache:
            self.__clear_artworks_cache = True
            self.__clear_agents_cache = True
            self.__clear_galleries_cache = True
            self.__clear_exhibitions_cache = True
            self.__clear_catalogues_cache = True
            
        self.__artworks_cache = None
        self.__agents_cache = None
        self.__galleries_cache = None
        self.__exhibitions_cache = None
        self.__catalogues_cache = None
        
    def get_artworks(self) -> (pd.DataFrame, int, int, int):
        """
        Gets a list of artworks sorted by last updated date in descending order.
        
        Returns
        -------
        tuple
            A tuple of four elements represending a pandas DataFrame containing the
            transformed json results from the RESTful API, the max page of a multi-page
            set of return data from the public API, the total number of pages and the
            total number of records in all of the artworks data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> artworks_df, current_page, total_pages, total = art_api_client.get_artworks()
        """
        self.__artworks_cache, self.__clear_artworks_cache, data_df, current_page, total_pages, total = self.__get_data(
            self.__artworks_cache,
            self.__clear_artworks_cache,
            ActionType.ARTWORKS,
            ['id', 'title', 'date_display', 'place_of_origin', 'artist_ids', 'artist_titles']
        )        
        return data_df, current_page, total_pages, total
    
    def get_artists(self) -> (pd.DataFrame, int, int, int):
        """
        Gets a list of all artists sorted by last updated date in descending order.
        
        Returns
        -------
        tuple
            A tuple of four elements represending a pandas DataFrame containing the
            transformed json results from the RESTful API, the max page of a multi-page
            set of return data from the public API, the total number of pages and the
            total number of records in all of the artists data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> artists_df, current_page, total_pages, total = art_api_client.get_artists()
        """
        self.__agents_cache, self.__clear_agents_cache, data_df, current_page, total_pages, total = self.__get_data(
            self.__agents_cache,
            self.__clear_agents_cache,
            ActionType.AGENTS,
            ['id', 'title', 'is_artist', 'artwork_ids']
        )
        data_df = data_df.loc[data_df['is_artist'] == True]
        return data_df, current_page, total_pages, total
    
    def get_galleries(self, exclude_closed:bool = True) -> (pd.DataFrame, int, int, int):
        """
        Gets a list of all galleries sorted by last updated date in descending order.
        
        Parameters
        ----------
        exclude_closed: bool, optional
            True returns data with closed galleries excluded. Otherwise, data
            will include closed galleries as well. Default value is True.
        
        Returns
        -------
        tuple
            A tuple of four elements represending a pandas DataFrame containing the
            transformed json results from the RESTful API, the max page of a multi-page
            set of return data from the public API, the total number of pages and the
            total number of records in all of the galleries data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> galleries_df, current_page, total_pages, total = art_api_client.get_galleries()
        """
        self.__galleries_cache, self.__clear_galleries_cache, data_df, current_page, total_pages, total = self.__get_data(
            self.__galleries_cache,
            self.__clear_galleries_cache,
            ActionType.GALLERIES,
            ['id', 'title', 'type', 'is_closed', 'latlon']
        )
        if exclude_closed:
            data_df = data_df.loc[data_df['is_closed'] == False]
        return data_df, current_page, total_pages, total
    
    def get_exhibitions(self, exclude_closed:bool = True) -> (pd.DataFrame, int, int, int):
        """
        Gets a list of all exhibitions sorted by last updated date in descending order.
        
        Parameters
        ----------
        exclude_closed: bool, optional
            True returns data with closed exhibitions excluded. Otherwise, data
            will include closed exhibitions as well. Default value is True.
        
        Returns
        -------
        tuple
            A tuple of four elements represending a pandas DataFrame containing the
            transformed json results from the RESTful API, the max page of a multi-page
            set of return data from the public API, the total number of pages and the
            total number of records in all of the exhibitions data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> exhibitions_df, current_page, total_pages, total = art_api_client.get_exhibitions()
        """
        self.__exhibitions_cache, self.__clear_exhibitions_cache, data_df, current_page, total_pages, total = self.__get_data(
            self.__exhibitions_cache,
            self.__clear_exhibitions_cache,
            ActionType.EXHIBITIONS,
            ['id', 'title', 'short_description', 'status', 'artwork_ids', 'artist_ids'] # 'is_featured', 'gallery_id', 'type',
        )
        if exclude_closed:
            data_df = data_df.loc[data_df['status'] != 'Closed']
        return data_df, current_page, total_pages, total
    
    def get_catalogues(self) -> (pd.DataFrame, int, int, int):
        """
        Gets a list of all catalogues sorted by last updated date in descending order.
        
        Returns
        -------
        tuple
            A tuple of four elements represending a pandas DataFrame containing the
            transformed json results from the RESTful API, the max page of a multi-page
            set of return data from the public API, the total number of pages and the
            total number of records in all of the catalogues data.
        
        Examples
        --------
        >>> from artsapiclient_ds3478 import ArtInstChicagoApiClient
        >>> art_api_client = ArtInstChicagoApiClient(use_internal_cache = True)
        >>> catalogues_df, current_page, total_pages, total = art_api_client.get_catalogues()
        """
        self.__catalogues_cache, self.__clear_catalogues_cache, data_df, current_page, total_pages, total = self.__get_data(
            self.__catalogues_cache,
            self.__clear_catalogues_cache,
            ActionType.CATALOGUES,
            ['id', 'title']
        )        
        return data_df, current_page, total_pages, total
