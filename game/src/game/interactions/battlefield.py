from src.game.subjects.user import User
from src.game.subjects.enemy import Enemy


class Battlefield:
    def __init__(self,
                 user: User = None,
                 enemy: Enemy = None,
                 user_factory: any = None,
                 enemy_factory: any = None) -> None:

        self._user = user
        self._enemy = enemy
        self._user_factory = user_factory
        self._enemy_factory = enemy_factory

    def get_user(self) -> User:
        return self._user

    def get_enemy(self) -> Enemy:
        return self._enemy

    def make_turn(self) -> bool:
        self._user.attack(self._enemy)

        if self._enemy.dead_check():
            self._enemy_factory.update_dead(
                enemy=self._enemy
            )

            return False

        self._enemy_factory.update_hp(
            enemy=self._enemy
        )

        self._enemy.attack(self._user)

        self._user_factory.update_hp(
            user=self._user
        )

        return True
