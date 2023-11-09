import json
import os

from service.query_builder import QueryBuilder


class AeroDataBox(QueryBuilder):
    def __init__(self):
        super().__init__(headers=self.get_header(), url=self._url())

    @staticmethod
    def _url() -> str | None:
        return os.getenv('AERO_DATA_API')

    @staticmethod
    def _token() -> str | None:
        return os.getenv('AERO_DATA_KEY')

    def get_header(self) -> dict:
        return {"X-RapidAPI-Key": self._token(), "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}
