from datetime import datetime

from src.game.constructor.connector import BaseConnector


class CommandCenterConnector(BaseConnector):
    def __init__(
        self,
        host: str = None,
        port: str = None,
        database: str = None,
        connection_type: str = None,
        username: str = None,
        password: str = None
    ) -> None:

        super().__init__(
            host=host,
            port=port,
            database=database,
            connection_type=connection_type,
            username=username,
            password=password
        )

    def load_commands(self,
                      current_dttm: datetime = None) -> tuple[list, list]:
        data_cols, data_vals = self.execute(f"""
            SELECT
                id as command,
                descr as command_descr
            FROM dbo.commands
            WHERE end_dttm > '{current_dttm}'
                and start_dttm <= '{current_dttm}';
        """, fetch_results=True)
        return data_cols, data_vals

    def load_comman_descr(self,
                          command: str = None,
                          current_dttm: datetime = None) -> tuple[list, list]:
        data_cols, data_vals = self.execute(f"""
            SELECT
                s.attribute as attribute,
                s.descr as attribute_descr
            FROM dbo.commands c
            LEFT JOIN dbo.satt_commands__attributes s
                ON c.id = s.id
            WHERE c.id = '{command}'
                and c.end_dttm > '{current_dttm}'
                and c.start_dttm <= '{current_dttm}'
                and s.valid_from <= '{current_dttm}'
                and s.valid_to > '{current_dttm}';
        """, fetch_results=True)
        return data_cols, data_vals

    def load_states(self,
                    current_dttm: datetime = None) -> tuple[list, list]:
        data_cols, data_vals = self.execute(f"""
            SELECT
                id as state,
                descr as descr
            FROM dbo.states
            WHERE end_dttm > '{current_dttm}'
                and start_dttm <= '{current_dttm}'
        """, fetch_results=True)
        return data_cols, data_vals
