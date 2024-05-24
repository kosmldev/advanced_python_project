class Castable(object):
    def __init__(
            self,
            known_spells: list = None,
            **kwargs) -> None:
        self._known_spells = known_spells

    def cast_spell_on(self,
                      spell_name: str = None,
                      target: any = None) -> None:
        if self._known_splles.get(spell_name) is not None:
            self._known_splles.get(spell_name).affect(target)
        else:
            print('Spell is unknown')
            raise ValueError
