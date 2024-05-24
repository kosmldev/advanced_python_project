class Earnable(object):

    def __init__(self,
                 profit: int = None,
                 profit_type: str = None,
                 **kwargs) -> None:
        self._profit = profit
        self._profit_type = profit_type

    def get_profit(self) -> int:
        return self._profit

    def get_profit_type(self) -> int:
        return self._profit_type
