from datetime import datetime

from src.game.constructor.connector import BaseConnector


class GreedfieldActionConnector(BaseConnector):
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

    def create_greedfield(self,
                          user_id: str = None,
                          greed_id: str = None,
                          current_dttm: datetime = None) -> None:
        self.execute(f"""
            INSERT INTO dbo.link_greeds__users (
                greed_id, user_id, dttm, is_actual
            )
            VALUES
                ('{greed_id}', '{user_id}', '{current_dttm}', 1::boolean);
        """)

    def end_greedfield(self,
                       user_id: str = None,
                       greed_id: str = None) -> None:
        self.execute(f"""
            UPDATE dbo.link_greeds__users
            SET is_actual = 0::boolean
            WHERE user_id = '{user_id}' and greed_id='{greed_id}';
        """)

    def load_greedfield_greed(self,
                              user_id: str = None) -> tuple[list, list]:
        greed_cols, greed_vals = self.execute(f"""
            SELECT
                greed_id as unique_identifier
            FROM dbo.link_greeds__users
            WHERE user_id = '{user_id}' and is_actual = 1::boolean;
        """, fetch_results=True)
        return greed_cols, greed_vals
