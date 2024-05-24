from src.game.constructor.earnable import Earnable
from src.game.constructor.namable import Nameble

PROFIT_TYPE_DICT = {
    'experiance': 'экспа',
    'mana': 'мана',
    'hp': 'хэпешечка',
    'l_attack': 'нижняя граница урона',
    'u_attack': 'верхняя граница урона',
}


class Greed(Earnable, Nameble):

    def __init__(self,
                 name: str = None,
                 unique_identifier: str = None,
                 profit: int = None,
                 profit_type: str = None,
                 **kwargs
                 ) -> None:

        Nameble.__init__(self,
                         name=name,
                         unique_identifier=unique_identifier,
                         **kwargs)

        Earnable.__init__(self,
                          profit=profit,
                          profit_type=profit_type,
                          **kwargs)

    def verbose(self) -> str:
        out_ = ''
        out_ += f'Имя: {self._name}\n'
        out_ += f'Что повышает: {PROFIT_TYPE_DICT.get(self._profit_type)}\n'
        out_ += f'Насколько повышает: {self._profit_type}'
        return out_
