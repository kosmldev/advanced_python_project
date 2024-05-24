class Nameble(object):

    def __init__(self,
                 name: str = None,
                 unique_identifier: str = None,
                 **kwargs) -> None:
        self._name = name
        self._unique_identifier = unique_identifier

    def update_name(self, new_name: str = None) -> None:
        self._name = new_name

    def get_id(self) -> str:
        return self._unique_identifier

    def get_name(self) -> str:
        return self._name

    def verbose(self) -> str:
        return self.__dict__
