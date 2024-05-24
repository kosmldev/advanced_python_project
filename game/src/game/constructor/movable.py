class Movable(object):
    def __init__(self,
                 loc: any = None,
                 **kwargs) -> None:
        self._loc = loc

    def get_loc(self) -> any:
        return self._loc

    def move_to(self,
                loc: any = None) -> None:
        self._loc = loc
