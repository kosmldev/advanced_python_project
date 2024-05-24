import datetime

from src.game.constructor.factories import BaseFactory
from src.game.connectors.greedfield_connector import GreedfieldActionConnector
from src.game.interactions.greedfield import Greedfield
from .user_factory import UserFactoryUpdater
from .greed_factory import GreedFactory
from src.game.subjects.user import User
from src.game.subjects.greed import Greed


class GreedfieldFactory(BaseFactory):
    def __init__(self,
                 connector: GreedfieldActionConnector = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def create_greedfield(self,
                          user: User = None,
                          greed: Greed = None,
                          user_updater: UserFactoryUpdater = None,
                          greed_updater: GreedFactory = None) -> Greedfield:
        now_datetime = datetime.datetime.now()

        self._connector.create_greedfield(
            user_id=user.get_id(),
            greed_id=greed.get_id(),
            current_dttm=now_datetime
        )

        return Greedfield(
            user=user,
            greed=greed,
            user_factory=user_updater,
            greed_factory=greed_updater
        )

    def load_greedfield(self,
                        user: User = None,
                        user_updater: UserFactoryUpdater = None,
                        greed_updater: GreedFactory = None) -> GreedFactory:

        data_cols, data_vals = self._connector.load_greedfield_greed(
            user_id=user.get_id()
        )

        enemy_info = {
            list(data_cols)[i]: list(data_vals)[0][i]
            for i in range(len(list(data_cols)))
            }

        greed = greed_updater.load_existed_greed(
            unique_identifer=enemy_info.get('unique_identifier')
        )

        return Greedfield(
            user=user,
            greed=greed,
            user_factory=user_updater,
            greed_factory=greed_updater
        )

    def end_greedfield(self,
                       greedfield: Greedfield = None) -> None:
        self._connector.end_greedfield(
            user_id=greedfield.get_user().get_id(),
            greed_id=greedfield.get_greed().get_id()
        )
