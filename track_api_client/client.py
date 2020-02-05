import typing
import copy
import json

import requests
from requests.exceptions import RequestException

from .constants import API_KEY_HEADER
from . import exceptions
from .apitypes import ApiTypeTrackPoint, convert_api_resp_points


class ApiClient:
    default_client_request_options = {}

    def __init__(
         self, base_url: str, api_key: str, api_key_header: str = None,
            request_default_options: typing.Optional[dict] = None
    ):
        self.base_url = base_url
        self.api_key = api_key
        if not api_key_header:
            api_key_header = API_KEY_HEADER
        self.api_key_header = api_key_header
        if not request_default_options:
            request_default_options = {}
        self.request_default_options = request_default_options

    def get_track_points(
            self, terminal_id: int, start_at: int, finish_at: int = None, limit: int = None, offset: int = 0,
            order_asc: bool = True
    ) -> typing.List[ApiTypeTrackPoint]:
        resp = self.call_method(
            'get_track_points',
            params={
                'terminal_id': terminal_id, 'start_at': start_at, 'finish_at': finish_at,
                'limit': limit, 'offset': offset, 'order_asc': int(order_asc)
            }
        )
        return convert_api_resp_points(resp, terminal_id)

    def get_filtered_track_points(
            self, terminal_id: int, start_at: int, finish_at: int, granularity: int
    ) -> typing.List[ApiTypeTrackPoint]:
        resp = self.call_method(
            'get_filtered_track_points',
            params={
                'terminal_id': terminal_id, 'start_at': start_at, 'finish_at': finish_at,
                'granularity': granularity
            }
        )
        return convert_api_resp_points(resp, terminal_id)

    def get_first_track_point(
            self, terminal_id: int, start_at: int, finish_at: int = None
    ) -> typing.Optional[ApiTypeTrackPoint]:
        points = self.get_track_points(
            terminal_id, start_at, finish_at, limit=1, order_asc=True
        )
        if points:
            return points[0]

    def get_last_track_point(
            self, terminal_id: int, start_at: int, finish_at: int = None
    ) -> typing.Optional[ApiTypeTrackPoint]:
        points = self.get_track_points(
            terminal_id, start_at, finish_at, limit=1, order_asc=False
        )
        if points:
            return points[0]

    def call_method(self, method_name: str, method_type: str = 'get', params: typing.Optional[typing.Dict] = None,
                    request_options: typing.Optional[typing.Dict] = None):
        resp_data = None

        try:
            request_options = self.get_request_options(request_options)
            if not params:
                params = {}
            request_options['params'] = params
            r = requests.request(method_type, self.base_url + method_name, **request_options)
        except RequestException as e:
            raise exceptions.ApiClientException(
                method_type, 'Requests exception', details=str(e), request=request_options
            )

        self.handle_status(r, method_name, request_options)

        try:
            resp_data = r.json()
        except json.JSONDecodeError as e:
            raise exceptions.ApiClientException(
                method_type, 'Decode response error', request=request_options, response=resp_data
            )

        return resp_data

    def handle_status(self, response, method_name: str, request_options: typing.Optional[typing.Dict] = None):
        status = self.get_status(response)
        if status == 200:
            return
        ex_class = exceptions.ApiClientException
        if status == 400:
            ex_class = exceptions.ApiClientBadRequest
        if status == 401:
            ex_class = exceptions.ApiClientUnauthorized
        raise ex_class(method_name, request=request_options, response=response)

    def get_status(self, response: requests.Response):
        return response.status_code

    def get_request_options(self, request_options: typing.Optional[typing.Dict] = None) -> typing.Dict:
        options = self.get_request_default_options()
        if request_options:
            options.update(request_options)
        return options

    def get_request_default_options(self) -> typing.Dict:
        default_options = copy.deepcopy(self.request_default_options)
        default_options['headers'] = {
            self.api_key_header: self.api_key,
        }
        return default_options
