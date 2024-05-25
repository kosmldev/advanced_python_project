import numpy as np

from src.game.constructor.namable import Nameble


class Location(Nameble):

    def __init__(self,
                 name: str = None,
                 unique_identifier: str = None,
                 possible_enemies: list = None,
                 possible_enemies_ratio: list = None,
                 possible_greeds: list = None,
                 possible_greeds_ratio: list = None,
                 **kwargs) -> None:
        super().__init__(
            name=name,
            unique_identifier=unique_identifier,
            **kwargs
        )
        self._possible_enemies = possible_enemies
        self._possible_enemies_ratio = possible_enemies_ratio
        self._possible_greeds = possible_greeds
        self._possible_greeds_ratio = possible_greeds_ratio

    def get_possible_enemies(self) -> tuple[list, list]:
        return self._possible_enemies, self._possible_enemies_ratio

    def get_possible_greeds(self) -> tuple[list, list]:
        return self._possible_greeds, self._possible_greeds_ratio

    def verbose(self) -> str:
        out_ = ''
        out_ += f'Имя: {self._name}\n'
        out_ += 'Противники:\n'
        for one_i in range(len(self._possible_enemies)):
            out_ += f'Имя: {self._possible_enemies[one_i]} с шансом '
            out_ += f'{np.round(self._possible_enemies_ratio[one_i]*100, 1)}%\n'
        out_ += '\n'
        out_ += 'Плюшки:\n'
        for one_i in range(len(self._possible_greeds_ratio)):
            out_ += f'Имя: {self._possible_greeds[one_i]} с шансом '
            out_ += f'{np.round(self._possible_greeds_ratio[one_i]*100, 1)}%\n'
        out_ = out_[:-1]
        return out_
