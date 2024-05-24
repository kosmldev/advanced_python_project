from datetime import datetime

from src.game.constructor.connector import BaseConnector


class GreedFactoryConnector(BaseConnector):
    def __init__(
        self,
        host: str = None,
        port: str = None,
        database: str = None,
        connection_type: str = None,
        username: str = None,
        password: str = None,
        **kwargs
    ) -> None:

        super().__init__(
            host=host,
            port=port,
            database=database,
            connection_type=connection_type,
            username=username,
            password=password,
            **kwargs
        )

    def push_new_greed(self,
                       id: str,
                       dttm_created: datetime,
                       dttm_updated: datetime,
                       update_identifier: str,
                       value: int) -> None:
        self.execute(f"""
            INSERT INTO dbo.greeds (
                id,
                dttm_created,
                dttm_updated,
                update_identifier,
                value
                )
            VALUES (
                '{id}',
                '{dttm_created}',
                '{dttm_updated}',
                '{update_identifier}',
                {value});
        """)

    def get_greed_info(self,
                       start_dttm: datetime,
                       end_dttm: datetime,
                       name: str) -> tuple[list, list]:
        columns, rows = self.execute(f"""
            SELECT
                id as base_id,
                value as profit,
                update_identifier as profit_type
            FROM dbo.base_greeds
            WHERE start_dttm <= '{start_dttm}'
                and end_dttm > '{end_dttm}'
                and name = '{name}';
            """, fetch_results=True)
        return columns, rows

    def get_greed(self, unique_identifer: str) -> tuple[list, list]:
        columns, rows = self.execute(f"""
            SELECT
                b.name as name,
                en.id as unique_identifier,
                en.value as profit,
                en.update_identifier as profit_type
            FROM dbo.greeds en
            INNER JOIN dbo.link_greeds__base_greeds l on en.id = l.greed_id
            INNER JOIN dbo.base_greeds b on b.id = l.base_id
            WHERE en.id = '{unique_identifer}'
                and l.is_actual = 1::boolean;
            """, fetch_results=True)
        return columns, rows

    def push_new_greed_link(self,
                            base_id: str = None,
                            greed_id: str = None,
                            dttm: datetime = None) -> None:

        self.execute(f"""
            INSERT INTO dbo.link_greeds__base_greeds (
                base_id,
                greed_id,
                dttm,
                is_actual)
            VALUES (
                '{base_id}',
                '{greed_id}',
                '{dttm}',
                1::boolean);
        """)
