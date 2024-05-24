import datetime
import hashlib
from random import getrandbits


from src.game.constructor.factories import BaseFactory
from src.game.connectors.enemy_connector import EnemyFactoryConnector
from src.game.subjects.enemy import Enemy
from src.game.subjects.location import Location


import numpy as np


class EnemyFactory(BaseFactory):

    def __init__(self,
                 connector: EnemyFactoryConnector = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def load_existed_enemy(self,
                           unique_identifer: str = None) -> Enemy:

        enemy_info_cols, enemy_info_values = self._connector.get_enemy(
            unique_identifer
            )

        enemy_info = {
            list(enemy_info_cols)[i]: list(enemy_info_values)[0][i]
            for i in range(len(list(enemy_info_cols)))
            }

        return Enemy(**enemy_info)

    def create_random_new_enemy(self,
                                loc: Location = None) -> Enemy:
        possible_enemies, ratio = loc.get_possible_enemies()

        enemy_name = np.random.choice(possible_enemies, size=1, p=ratio)[0]

        now_datetime = datetime.datetime.now()

        enemy_info_cols, enemy_info_values = self._connector.get_enemy_info(
            start_dttm=now_datetime,
            end_dttm=now_datetime,
            name=enemy_name
        )

        enemy_info = {
            list(enemy_info_cols)[i]: list(enemy_info_values)[0][i]
            for i in range(len(list(enemy_info_cols)))
            }

        random_hash = getrandbits(128)

        md5_unique_identifier = hashlib.md5(
            bytes(f"{now_datetime}_{random_hash}", encoding='utf-8')
            ).hexdigest()

        self._connector.push_new_enemy(
            id=md5_unique_identifier,
            dttm_created=now_datetime,
            dttm_updated=now_datetime,
            hp=enemy_info.get('hp'),
            l_atck=enemy_info.get('attack_power_lower'),
            u_atck=enemy_info.get('attack_power_upper'),
            is_dead=0
        )

        self._connector.push_new_enemy_link(
            base_id=enemy_info.get('base_id'),
            enemy_id=md5_unique_identifier,
            dttm=now_datetime
        )

        del enemy_info['base_id']

        enemy_kwargs = {
            'name': enemy_name,
            'unique_identifier': md5_unique_identifier
        }
        return Enemy(**{**enemy_info, **enemy_kwargs})

    def update_hp(self,
                  enemy: Enemy = None) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_hp(
            unique_identifier=enemy._unique_identifier,
            new_hp=enemy._hp,
            current_dttm=now_datetime
        )

    def update_dead(self,
                    enemy: Enemy = None) -> None:
        now_datetime = datetime.datetime.now()

        self._connector.update_dead(
            unique_identifier=enemy._unique_identifier,
            current_dttm=now_datetime
        )
