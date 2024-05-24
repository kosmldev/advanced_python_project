from datetime import datetime


from src.game.constructor.factories import BaseConnector


class UserFactoryConnectorUpdater(BaseConnector):
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

    def check_if_pass_can_be_changed(self,
                                     unique_identifier: str = None,
                                     previous_pass: str = None,
                                     **kwargs) -> tuple[list, list]:
        pass_cols, pass_vals = self.execute(f"""
            SELECT
                1 as its_ok
            FROM dbo.satt_users__password sup
            WHERE user_id = '{unique_identifier}'
                and password = '{previous_pass}'
                and valid_from = (
                    SELECT
                        max(valid_from)
                    FROM dbo.satt_users__password
                    WHERE user_id = '{unique_identifier}'
                );
        """, fetch_results=True)
        return pass_cols, pass_vals

    def update_user_password(self,
                             unique_identifier: str = None,
                             new_pass: str = None,
                             current_dttm: datetime = None,
                             **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__password SET valid_to = '{current_dttm}'
            WHERE user_id = '{unique_identifier}'
                and valid_from = (
                    SELECT
                        max(valid_from)
                    FROM dbo.satt_users__password
                    WHERE user_id = '{unique_identifier}'
                );
            INSERT INTO dbo.satt_users__password (user_id, password,
                valid_from, valid_to)
            VALUES ('{unique_identifier}', '{new_pass}', '{current_dttm}',
                '2050-01-01'::timestamp);
        """)

    def update_user_name(self,
                         unique_identifier: str = None,
                         new_name: str = None,
                         current_dttm: datetime = None,
                         **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__name SET valid_to = '{current_dttm}'
            WHERE user_id = '{unique_identifier}'
                and valid_from = (
                    SELECT
                        max(valid_from)
                    FROM dbo.satt_users__name
                    WHERE user_id = '{unique_identifier}'
                );
            INSERT INTO dbo.satt_users__name (user_id, name,
                valid_from, valid_to)
            VALUES ('{unique_identifier}', '{new_name}', '{current_dttm}',
                '2050-01-01'::timestamp);
        """)

    def update_hp(self,
                  unique_identifier: str = None,
                  new_hp: int = None,
                  current_dttm: datetime = None,
                  **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__base_stats SET hp = {new_hp}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__base_stats
                SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_mana(self,
                    unique_identifier: str = None,
                    new_mana: int = None,
                    current_dttm: datetime = None,
                    **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__base_stats SET mana = {new_mana}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__base_stats
                SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_attack(self,
                      unique_identifier: str = None,
                      new_l_atck: int = None,
                      new_u_atck: int = None,
                      current_dttm: datetime = None,
                      **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__attck SET l_atck = {new_l_atck}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__attck SET u_atck = {new_u_atck}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__attck SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_balance(self,
                       unique_identifier: str = None,
                       new_balance: float = None,
                       current_dttm: datetime = None,
                       **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__adv_stats SET balance = {new_balance}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__adv_stats
                SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_experiance(self,
                          unique_identifier: str = None,
                          new_experiance: float = None,
                          current_dttm: datetime = None,
                          **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__adv_stats SET experiance = {new_experiance}
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__adv_stats
                SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_state(self,
                     unique_identifier: str = None,
                     new_state: int = None,
                     current_dttm: datetime = None,
                     **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.satt_users__current_state SET state = {new_state}::int2
            WHERE user_id = '{unique_identifier}';
            UPDATE dbo.satt_users__current_state
                SET dttm_updated = '{current_dttm}'
            WHERE user_id = '{unique_identifier}';
        """)

    def update_location(self,
                        unique_identifier: str = None,
                        new_location: int = None,
                        current_dttm: datetime = None,
                        **kwargs) -> None:
        self.execute(f"""
            UPDATE dbo.link_users__locations SET is_actual = 0::boolean
            WHERE user_id = '{unique_identifier}' and is_actual = 1::boolean;
            INSERT INTO dbo.link_users__locations (
                loc_id, user_id, dttm, is_actual
            )
            VALUES
                ('{new_location}', '{unique_identifier}',
                '{current_dttm}', 1::boolean);
        """)


class UserFactoryConnectorBaseInfo(BaseConnector):
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

    def get_data_for_new_user(self,
                              current_dttm: datetime = None,
                              **kwargs) -> tuple[list, list]:

        actual_init_cols, actual_init_vals = self.execute(f"""
            SELECT
                hp,
                mana,
                balance,
                experiance,
                l_atck as attack_power_lower,
                u_atck as attack_power_upper,
                default_location as loc_id
            FROM dbo.users_template u
            WHERE start_dttm <= '{current_dttm}'
                and end_dttm > '{current_dttm}'
        """, fetch_results=True)

        return actual_init_cols, actual_init_vals

    def create_new_user(self,
                        unique_identifier: str = None,
                        loc_id: str = None,
                        username: str = None,
                        password_md5: str = None,
                        current_dttm: datetime = None,
                        end_dttm: datetime = None,
                        hp: int = None,
                        mana: int = None,
                        balance: int = None,
                        experiance: float = None,
                        attack_power_upper: int = None,
                        attack_power_lower: int = None,
                        **kwargs) -> None:
        self.execute(f"""
            INSERT INTO dbo.users (id, start_dttm, end_dttm)
            VALUES
                ('{unique_identifier}', '{current_dttm}', '{end_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.link_users__locations (loc_id, user_id,
                     dttm, is_actual)
            VALUES
                ('{loc_id}', '{unique_identifier}',
                 '{current_dttm}', 1::boolean);
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__password (user_id, password,
                     valid_from, valid_to)
            VALUES
                ('{unique_identifier}', '{password_md5}', '{current_dttm}',
                 '{end_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__name (user_id, name, valid_from,
                     valid_to)
            VALUES
                ('{unique_identifier}', '{username}', '{current_dttm}',
                 '{end_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__base_stats (user_id, hp, mana,
                     dttm_created, dttm_updated)
            VALUES
                ('{unique_identifier}', {hp}, {mana}, '{current_dttm}',
                 '{current_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__attck (user_id, l_atck, u_atck,
                     dttm_created, dttm_updated)
            VALUES
                ('{unique_identifier}', {attack_power_lower},
                 {attack_power_upper}, '{current_dttm}', '{current_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__adv_stats (user_id, balance,
                     experiance, dttm_created, dttm_updated)
            VALUES
                ('{unique_identifier}', {balance}, {experiance},
                 '{current_dttm}', '{current_dttm}');
        """)

        self.execute(f"""
            INSERT INTO dbo.satt_users__current_state (user_id, state,
                     dttm_created, dttm_updated)
            VALUES
                ('{unique_identifier}', 1::int2, '{current_dttm}',
                 '{end_dttm}');
        """)

    def authorize(self,
                  username: str = None,
                  password: str = None,
                  current_dttm: datetime = None,
                  **kwargs) -> tuple[list, list]:
        cols, vals = self.execute(f"""
            SELECT
                us.id as unique_identifier
            FROM dbo.satt_users__name sun
            INNER JOIN dbo.users us on us.id = sun.user_id
            INNER JOIN dbo.satt_users__password sup on sup.user_id = us.id
            WHERE sun.name = '{username}' and sup.password = '{password}'
                and sun.valid_from <= '{current_dttm}'
                and sun.valid_to > '{current_dttm}'
                and sup.valid_from <= '{current_dttm}'
                and sup.valid_to > '{current_dttm}'
                and us.start_dttm <= '{current_dttm}'
                and us.end_dttm > '{current_dttm}';
        """, fetch_results=True)
        return cols, vals

    def load_user_data(self,
                       unique_identifier: str = None,
                       current_dttm: datetime = None,
                       **kwargs) -> tuple[list, list]:

        user_cols, user_vals = self.execute(f"""
            SELECT
                sun.name,
                subs.hp,
                subs.mana,
                sua.l_atck as attack_power_lower,
                sua.u_atck as attack_power_upper,
                suas.balance,
                suas.experiance,
                sucs.state
            FROM dbo.users us
            INNER JOIN dbo.satt_users__name sun on sun.user_id = us.id
            INNER JOIN dbo.satt_users__base_stats subs on subs.user_id = us.id
            INNER JOIN dbo.satt_users__attck sua on sua.user_id = us.id
            INNER JOIN dbo.satt_users__adv_stats suas on suas.user_id = us.id
            INNER JOIN dbo.satt_users__current_state sucs
                on sucs.user_id = us.id
            WHERE us.id = '{unique_identifier}'
                and sun.valid_from <= '{current_dttm}'
                and sun.valid_to > '{current_dttm}'
                and us.start_dttm <= '{current_dttm}'
                and us.end_dttm > '{current_dttm}';
        """, fetch_results=True)
        return user_cols, user_vals

    def load_user_loc(self,
                      unique_identifier: str = None,
                      current_dttm: datetime = None,
                      **kwargs) -> tuple[list, list]:

        loc_cols, loc_vals = self.execute(f"""
            SELECT
                loc.name as loc
            FROM dbo.users us
            INNER JOIN dbo.link_users__locations l on l.user_id = us.id
            INNER JOIN dbo.locations loc on loc.id = l.loc_id
            WHERE us.id = '{unique_identifier}'
                and us.start_dttm <= '{current_dttm}'
                and us.end_dttm > '{current_dttm}'
                and loc.start_dttm <= '{current_dttm}'
                and loc.end_dttm > '{current_dttm}';
        """, fetch_results=True)
        return loc_cols, loc_vals
