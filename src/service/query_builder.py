import os

import requests


class QueryBuilder:
    def __init__(self, headers, url=''):
        self.headers = headers
        self.url = url

    def get_response(cls, url: str = '', params: dict | None = None) -> dict | None:
        if not url:
            url = cls.url
        response = requests.get(url=url, headers=cls.headers, params=params)
        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.json()["message"]}')
            return None
        return response.json()
