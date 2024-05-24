from random import randint


class Fightable(object):
    def __init__(self,
                 hp: int = None,
                 attack_power_lower: int = None,
                 attack_power_upper: int = None,
                 **kwargs) -> None:
        self._hp = hp
        self._attack_power_lower = attack_power_lower
        self._attack_power_upper = attack_power_upper
        self._dead = False

    def get_hp(self) -> int:
        return self._hp

    def get_attack_power_lower(self) -> int:
        return self._attack_power_lower

    def get_attack_power_upper(self) -> int:
        return self._attack_power_upper

    def take_damage(self,
                    damage: int = None) -> None:
        self._hp -= damage

    def attack(self,
               enemy: any = None) -> None:
        enemy.take_damage(
            randint(self._attack_power_lower, self._attack_power_upper)
            )

    def dead_check(self) -> bool:
        if self._hp < 0:
            self._dead = True

        return self._dead
