from src.game.constructor.fightable import Fightable
from src.game.constructor.namable import Nameble


class Enemy(Fightable, Nameble):

    def __init__(self,
                 name: str = None,
                 unique_identifier: str = None,
                 hp: int = None,
                 attack_power_lower: int = None,
                 attack_power_upper: int = None,
                 **kwargs
                 ) -> None:

        Nameble.__init__(self,
                         name=name,
                         unique_identifier=unique_identifier,
                         **kwargs)

        Fightable.__init__(self,
                           hp=hp,
                           attack_power_lower=attack_power_lower,
                           attack_power_upper=attack_power_upper,
                           **kwargs)

    def verbose(self) -> str:
        out_ = ''
        out_ += f'Имя: {self._name}\n'
        out_ += f'Атака: {self._attack_power_lower} '
        out_ += f'- {self._attack_power_upper}\n'
        out_ += f'HP: {self._hp}'
        return out_
