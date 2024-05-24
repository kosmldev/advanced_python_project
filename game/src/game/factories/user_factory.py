import datetime
import hashlib
from random import getrandbits


from src.game.constructor.factories import BaseFactory
from src.game.connectors.user_connector import (
    UserFactoryConnectorBaseInfo, UserFactoryConnectorUpdater
)
from src.game.subjects.user import User


class UserFactoryUpdater(BaseFactory):
    def __init__(self,
                 connector: UserFactoryConnectorUpdater = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def update_username(self,
                        user: User = None,
                        new_name: str = None) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_user_name(
            unique_identifier=user.get_id(),
            new_name=new_name,
            current_dttm=now_datetime
        )

    def update_password(self,
                        user: User = None,
                        old_pass: str = None,
                        new_pass: str = None) -> None:
        now_datetime = datetime.datetime.now()

        md5_old_pass = hashlib.md5(
            bytes(f"{old_pass}", encoding='utf-8')
            ).hexdigest()

        md5_new_pass = hashlib.md5(
            bytes(f"{new_pass}", encoding='utf-8')
            ).hexdigest()

        _, pass_vals = self._connector.check_if_pass_can_be_changed(
            unique_identifier=user.get_id(),
            previous_pass=md5_old_pass
        )

        if not pass_vals:
            print('Неверный старый пароль, невозможно обновить')
            return None

        self._connector.update_user_password(
            unique_identifier=user.get_id(),
            new_pass=md5_new_pass,
            current_dttm=now_datetime
        )

    def update_hp(self,
                  user: User = None,
                  **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_hp(
            unique_identifier=user.get_id(),
            new_hp=user.get_hp(),
            current_dttm=now_datetime
        )

    def update_mana(self,
                    user: User = None,
                    **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_mana(
            unique_identifier=user.get_id(),
            new_mana=user.get_mana(),
            current_dttm=now_datetime
        )

    def update_attack(self,
                      user: User = None,
                      **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_attack(
            unique_identifier=user.get_id(),
            new_l_atck=user.get_attack_power_lower(),
            new_u_atck=user.get_attack_power_upper(),
            current_dttm=now_datetime
        )

    def update_balance(self,
                       user: User = None,
                       **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_balance(
            unique_identifier=user.get_id(),
            new_balance=user.get_balance(),
            current_dttm=now_datetime
        )

    def update_experiance(self,
                          user: User = None,
                          **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_experiance(
            unique_identifier=user.get_id(),
            new_experiance=user.get_experiance(),
            current_dttm=now_datetime
        )

    def update_state(self,
                     user: User = None,
                     **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_state(
            unique_identifier=user.get_id(),
            new_state=user.get_state(),
            current_dttm=now_datetime
        )

    def update_location(self,
                        user: User = None,
                        **kwargs) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_location(
            unique_identifier=user.get_id(),
            new_location=user._loc.get_id(),
            current_dttm=now_datetime
        )


class UserFactoryBaseInfo(BaseFactory):
    def __init__(self,
                 connector: UserFactoryConnectorBaseInfo = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def create_new_user(self,
                        username: str = None,
                        password: str = None,
                        **kwargs) -> User:

        now_datetime = datetime.datetime.now()

        random_hash = getrandbits(128)

        md5_unique_identifier = hashlib.md5(
            bytes(f"{now_datetime}_{random_hash}_{username}", encoding='utf-8')
            ).hexdigest()

        md5_password = hashlib.md5(
            bytes(f"{password}", encoding='utf-8')
            ).hexdigest()

        init_cols, init_vals = self._connector.get_data_for_new_user(
            current_dttm=now_datetime
            )

        user_info = {
            list(init_cols)[i]: list(init_vals)[0][i]
            for i in range(len(list(init_cols)))
            }

        user_add_info = {
            "current_dttm": now_datetime,
            "password_md5": md5_password,
            "username": username,
            "unique_identifier": md5_unique_identifier,
            "end_dttm": datetime.datetime(2050, 1, 1)
        }

        user_info = {**user_info, **user_add_info}

        self._connector.create_new_user(**user_info)

        user_info['name'] = user_info.get('username')

        return User(**user_info)

    def load_user(self,
                  username: str = None,
                  password: str = None) -> None:
        now_datetime = datetime.datetime.now()

        md5_password = hashlib.md5(
            bytes(f"{password}", encoding='utf-8')
            ).hexdigest()

        init_cols, init_vals = self._connector.authorize(
            username=username,
            password=md5_password,
            current_dttm=now_datetime
        )

        user_info = {
            list(init_cols)[i]: list(init_vals)[0][i]
            for i in range(len(list(init_cols)))
            }

        data_cols, data_vals = self._connector.load_user_data(
            unique_identifier=user_info.get('unique_identifier'),
            current_dttm=now_datetime
        )

        user_add_info = {
            list(data_cols)[i]: list(data_vals)[0][i]
            for i in range(len(list(data_cols)))
            }

        loc_cols, loc_vals = self._connector.load_user_loc(
            unique_identifier=user_info.get('unique_identifier'),
            current_dttm=now_datetime
        )

        user_loc_info = {
            list(loc_cols)[i]: list(loc_vals)[0][i]
            for i in range(len(list(loc_cols)))
            }

        user_info = {**user_info, **user_add_info, **user_loc_info}

        return User(**user_info)
