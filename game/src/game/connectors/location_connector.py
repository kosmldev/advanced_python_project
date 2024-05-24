from datetime import datetime


from src.game.constructor.connector import BaseConnector


class LocationFactoryConnector(BaseConnector):
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

    def get_location(self,
                     name: str,
                     start_dttm: datetime,
                     end_dttm: datetime) -> tuple[list, list]:

        columns, rows = self.execute(f"""
            SELECT
                id as unique_identifier
            FROM dbo.locations
            WHERE start_dttm <= '{start_dttm}'
                and end_dttm > '{end_dttm}'
                and name = '{name}';
        """, fetch_results=True)
        return columns, rows

    def get_possible_enemies(self,
                             unique_identifier: str) -> tuple[list, list]:

        columns, rows = self.execute(f"""
            SELECT
                b.name as name,
                l.chance_ratio
            FROM dbo.locations lc
            INNER JOIN dbo.link_locations__base_enemies l on l.loc_id = lc.id
            INNER JOIN dbo.base_enemies b on b.id = l.base_id
            WHERE lc.id = '{unique_identifier}'
                and l.is_actual = 1::boolean;
        """, fetch_results=True)
        return columns, rows

    def get_possible_greeds(self,
                            unique_identifier: str) -> tuple[list, list]:

        columns, rows = self.execute(f"""
            SELECT
                b.name as name,
                l.chance_ratio
            FROM dbo.locations lc
            INNER JOIN dbo.link_locations__base_greeds l on l.loc_id = lc.id
            INNER JOIN dbo.base_greeds b on b.id = l.base_id
            WHERE lc.id = '{unique_identifier}'
                and l.is_actual = 1::boolean;
        """, fetch_results=True)
        return columns, rows
