from .connector import BaseConnector


class BaseFactory(object):
    def __init__(self,
                 connector: BaseConnector = None,
                 **kwargs) -> None:
        self._connector = connector

    def load_existed(self,
                     unique_idenifier: str = None) -> any:
        """
        Loading of existed object

        Args:
            unique_idenifier (str, optional): Identifier of object

        Returns:
            any: some object, alredy existed in database
        """

    def create_new(self, **kwargs) -> any:
        """
        Generate new object by **kwargs, unique for each instance

        Returns:
            any: some object, new generated
        """

    def update_smth(self, **kwargs) -> any:
        """
        Update object properties in database using connector

        Returns:
            any: some anwer
        """
