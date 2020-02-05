import abc
from dataclasses import dataclass


class ApiType(metaclass=abc.ABCMeta):
    pass


@dataclass
class ApiTypeTrackPoint(ApiType):
    long: float
    lat: float
    timestamp: int
    terminal_id: int = None


def convert_api_resp_points(data: list, terminal_id: int):
    if not data:
        return []
    return [convert_api_resp_point(item, terminal_id) for item in data]


def convert_api_resp_point(data: list, terminal_id: int):
    return ApiTypeTrackPoint(data[0], data[1], data[2], terminal_id)