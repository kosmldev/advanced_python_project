from src.game.constructor.namable import Nameble
from src.game.constructor.fightable import Fightable
from src.game.constructor.can_earn import CanEarn
from src.game.constructor.movable import Movable

from .location import Location


class User(Nameble, Fightable, CanEarn, Movable):

    def __init__(self,
                 name: str = None,
                 unique_identifier: str = None,
                 hp: int = None,
                 attack_power_lower: int = None,
                 attack_power_upper: int = None,
                 balance: float = None,
                 experiance: int = None,
                 mana: int = None,
                 loc: Location = None,
                 state: int = None,
                 **kwargs) -> None:

        Nameble.__init__(self,
                         name=name,
                         unique_identifier=unique_identifier,
                         **kwargs)
        Fightable.__init__(self,
                           hp=hp,
                           attack_power_lower=attack_power_lower,
                           attack_power_upper=attack_power_upper,
                           **kwargs)
        CanEarn.__init__(self,
                         balance=balance,
                         experiance=experiance,
                         mana=mana,
                         **kwargs)
        Movable.__init__(self,
                         loc=loc)

        self._state = state

    def update_state(self, state: int = None) -> None:
        self._state = state

    def get_state(self) -> int:
        return self._state

    def up_hp(self, add: int = None) -> bool:
        if add > self._experiance:
            return False
        else:
            self.earn(
                profit=add,
                profit_type='hp'
            )
            self.earn(
                profit=-add,
                profit_type='experiance'
            )
            return True

    def up_mana(self, add: int = None) -> bool:
        if add > self._experiance:
            return False
        else:
            self.earn(
                profit=add,
                profit_type='mana'
            )
            self.earn(
                profit=-add,
                profit_type='experiance'
            )
            return True

    def up_attack(self, add: int = None, which: str = None) -> bool:
        if add > self._experiance or which not in ('l_attack', 'u_attack'):
            return False
        else:
            self.earn(
                profit=add,
                profit_type=which
            )

            self.earn(
                profit=-add,
                profit_type='experiance'
            )
            return True

    def verbose(self) -> str:
        out_ = ''
        out_ += f'Имя: {self._name}\n'
        out_ += f'Атака: {self._attack_power_lower} '
        out_ += f'- {self._attack_power_upper}\n'
        out_ += f'Мана: {self._mana}\n'
        out_ += f'Экспа: {self._experiance}\n'
        out_ += f'Баланс: {self._balance}\n'
        out_ += f'HP: {self._hp}'
        return out_
