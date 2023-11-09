import os

import sqlalchemy


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

    def truncate_df(self, schema: str):
        engine = sqlalchemy.create_engine(self.con())
        with engine.begin() as conn:
            conn.exec_driver_sql(f"TRUNCATE TABLE {schema}")
