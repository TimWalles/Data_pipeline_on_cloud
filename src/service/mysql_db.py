import os


class MySQL:
    def __init__(self) -> None:
        self.host = os.getenv('RD_HOST')
        self.user = os.getenv('RD_USER')
        self.schema = os.getenv('RD_SCHEMA')
        self.port = os.getenv('RD_PORT')

    @staticmethod
    def _token() -> str | None:
        return os.getenv('RD_KEY', '')

    def con(self):
        return f'mysql+pymysql://{self.user}:{self._token()}@{self.host}:{self.port}/{self.schema}'
