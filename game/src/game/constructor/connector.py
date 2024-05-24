# Work with data type
from typing import Union

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.expression import Executable


class BaseConnector(object):

    def __init__(
            self,
            host: str = None,
            port: str = None,
            database: str = None,
            connection_type: str = None,
            username: str = None,
            password: str = None
    ) -> None:
        self._host = host
        self._port = port
        self._database = database
        self._connection_type = connection_type
        self._username = username
        self._password = password

        self._engine = create_engine(
            URL.create(
                username=self._username,
                password=self._password,
                host=self._host,
                port=self._port,
                database=self._database,
                drivername=self._connection_type
            ),
        )

    def prepare_query(self, query_text: str) -> str:
        prepared_query = text(query_text)
        return prepared_query

    def execute(self, query: str,
                fetch_results: bool = False) -> Union[None, list]:
        if isinstance(query, str):
            prepared_query = self.prepare_query(query)
        elif isinstance(query, Executable):
            prepared_query = query
        else:
            raise TypeError(
                f'Wrong type of query argument: {type(query).__name__}'
                )

        if fetch_results:
            with self._engine.connect().execution_options(
                autocommit=True
            ) as connection:
                result_proxy = connection.execute(prepared_query)
                return result_proxy.keys(), result_proxy.fetchall()
        else:
            with self._engine.connect().execution_options(
                autocommit=True
            ) as connection:
                connection.execute(prepared_query)
                connection.commit()
