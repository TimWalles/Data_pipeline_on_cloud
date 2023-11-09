import json
import os

from service.query_builder import QueryBuilder


class OpenWeather(QueryBuilder):
    def __init__(self, headers=None):
        super().__init__(headers, url=self._url())

    @staticmethod
    def _url() -> str:
        return os.getenv('OPEN_WEATHER_API', '')

    @staticmethod
    def _token() -> str | None:
        return os.getenv('OPEN_WEATHER_KEY')

    @classmethod
    def get_params(cls, lat: float, lon: float, units: str = 'metric', cnt: int = 40):
        return {'lat': lat, 'lon': lon, 'units': units, 'cnt': cnt, 'appid': cls._token()}
