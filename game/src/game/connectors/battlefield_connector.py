from datetime import datetime

from src.game.constructor.connector import BaseConnector


class BattlefieldActionConnector(BaseConnector):
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

    def create_battlefield(self,
                           user_id: str = None,
                           enemy_id: str = None,
                           current_dttm: datetime = None) -> None:
        self.execute(f"""
            INSERT INTO dbo.link_enemies__users (
                enemy_id, user_id, dttm, is_actual
            )
            VALUES
                ('{enemy_id}', '{user_id}', '{current_dttm}', 1::boolean);
        """)

    def end_battlefield(self,
                        user_id: str = None,
                        enemy_id: str = None) -> None:
        self.execute(f"""
            UPDATE dbo.link_enemies__users
            SET is_actual = 0::boolean
            WHERE user_id = '{user_id}' and enemy_id='{enemy_id}';
        """)

    def load_battlefield_enemy(self,
                               user_id: str = None) -> tuple[list, list]:
        enemy_cols, enemy_vals = self.execute(f"""
            SELECT
                enemy_id as unique_identifier
            FROM dbo.link_enemies__users
            WHERE user_id = '{user_id}' and is_actual = 1::boolean;
        """, fetch_results=True)
        return enemy_cols, enemy_vals
