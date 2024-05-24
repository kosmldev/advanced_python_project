from datetime import datetime

from src.game.constructor.connector import BaseConnector


class EnemyFactoryConnector(BaseConnector):
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

    def push_new_enemy(self,
                       id: str,
                       dttm_created: datetime,
                       dttm_updated: datetime,
                       hp: int,
                       l_atck: int,
                       u_atck: int,
                       is_dead: int) -> None:
        self.execute(f"""
            INSERT INTO dbo.enemies (
                id,
                dttm_created,
                dttm_updated,
                hp,
                l_atck,
                u_atck,
                is_dead
                )
            VALUES (
                '{id}',
                '{dttm_created}',
                '{dttm_updated}',
                {hp},
                {l_atck},
                {u_atck},
                {is_dead}::boolean);
        """)

    def get_enemy_info(self,
                       start_dttm: datetime,
                       end_dttm: datetime,
                       name: str) -> tuple[list, list]:
        columns, rows = self.execute(f"""
            SELECT
                id as base_id,
                hp as hp,
                l_atck as attack_power_lower,
                u_atck as attack_power_upper
            FROM dbo.base_enemies
            WHERE start_dttm <= '{start_dttm}'
                and end_dttm > '{end_dttm}'
                and name = '{name}';
            """, fetch_results=True)
        return columns, rows

    def get_enemy(self, unique_identifer: str) -> tuple[list, list]:
        columns, rows = self.execute(f"""
            SELECT
                b.name as name,
                en.id as unique_identifier,
                en.hp as hp,
                en.l_atck as attack_power_lower,
                en.u_atck as attack_power_upper
            FROM dbo.enemies en
            INNER JOIN dbo.link_enemies__base_enemies l on en.id = l.enemy_id
            INNER JOIN dbo.base_enemies b on b.id = l.base_id
            WHERE en.id = '{unique_identifer}'
                and l.is_actual = 1::boolean;
            """, fetch_results=True)
        return columns, rows

    def push_new_enemy_link(self,
                            base_id: str = None,
                            enemy_id: str = None,
                            dttm: datetime = None) -> None:

        self.execute(f"""
            INSERT INTO dbo.link_enemies__base_enemies (
                base_id,
                enemy_id,
                dttm,
                is_actual)
            VALUES (
                '{base_id}',
                '{enemy_id}',
                '{dttm}',
                1::boolean);
        """)

    def update_hp(self,
                  unique_identifier: str = None,
                  new_hp: int = None,
                  current_dttm: datetime = None,
                  **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.enemies SET hp = {new_hp}
            WHERE id = '{unique_identifier}';
            UPDATE dbo.enemies
                SET dttm_updated = '{current_dttm}'
            WHERE id = '{unique_identifier}';
        """)

    def update_dead(self,
                    unique_identifier: str = None,
                    current_dttm: datetime = None,
                    **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.enemies SET is_dead = 1::boolean
            WHERE id = '{unique_identifier}';
            UPDATE dbo.enemies
                SET dttm_updated = '{current_dttm}'
            WHERE id = '{unique_identifier}';
        """)
