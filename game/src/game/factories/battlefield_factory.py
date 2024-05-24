import datetime

from src.game.constructor.factories import BaseFactory
from src.game.connectors.battlefield_connector import (
    BattlefieldActionConnector
)
from src.game.interactions.battlefield import Battlefield
from .user_factory import UserFactoryUpdater
from .enemy_factory import EnemyFactory
from src.game.subjects.user import User
from src.game.subjects.enemy import Enemy


class BattlefieldFactory(BaseFactory):
    def __init__(self,
                 connector: BattlefieldActionConnector = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def create_battlefield(self,
                           user: User = None,
                           enemy: Enemy = None,
                           user_updater: UserFactoryUpdater = None,
                           enemy_updater: EnemyFactory = None) -> Battlefield:
        now_datetime = datetime.datetime.now()

        self._connector.create_battlefield(
            user_id=user.get_id(),
            enemy_id=enemy.get_id(),
            current_dttm=now_datetime
        )

        return Battlefield(
            user=user,
            enemy=enemy,
            user_factory=user_updater,
            enemy_factory=enemy_updater
        )

    def load_battlefield(self,
                         user: User = None,
                         user_updater: UserFactoryUpdater = None,
                         enemy_updater: EnemyFactory = None) -> Battlefield:

        data_cols, data_vals = self._connector.load_battlefield_enemy(
            user_id=user.get_id()
        )

        enemy_info = {
            list(data_cols)[i]: list(data_vals)[0][i]
            for i in range(len(list(data_cols)))
            }

        enemy = enemy_updater.load_existed_enemy(
            unique_identifer=enemy_info.get('unique_identifier')
        )

        return Battlefield(
            user=user,
            enemy=enemy,
            user_factory=user_updater,
            enemy_factory=enemy_updater
        )

    def end_battlefield(self,
                        battlefield: Battlefield = None) -> None:
        self._connector.end_battlefield(
            user_id=battlefield.get_user().get_id(),
            enemy_id=battlefield.get_enemy().get_id()
        )
