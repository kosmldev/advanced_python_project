from src.game.subjects.user import User
from src.game.subjects.greed import Greed


class Greedfield:
    def __init__(self,
                 user: User = None,
                 greed: Greed = None,
                 user_factory: any = None,
                 greed_factory: any = None) -> None:

        self._user = user
        self._greed = greed
        self._user_factory = user_factory
        self._greed_factory = greed_factory

    def get_user(self) -> User:
        return self._user

    def get_greed(self) -> Greed:
        return self._greed

    def take_greed(self) -> bool:
        self._user.earn(
            profit=self._greed.get_profit(),
            profit_type=self._greed.get_profit_type()
        )
