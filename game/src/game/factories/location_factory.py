import datetime

from src.game.constructor.factories import BaseFactory
from src.game.connectors.location_connector import LocationFactoryConnector
from src.game.subjects.location import Location


class LocationFactory(BaseFactory):

    def __init__(self,
                 connector: LocationFactoryConnector = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def create_location(self,
                        name: str = None) -> Location:
        loc_kwargs = {"name": name}

        now_datetime = datetime.datetime.now()
        _, loc_info_vals = self._connector.get_location(
            name=name,
            start_dttm=now_datetime,
            end_dttm=now_datetime
        )
        loc_kwargs['unique_identifier'] = loc_info_vals[0][0]

        _, loc_enemies_vals = self._connector.get_possible_enemies(
            unique_identifier=loc_kwargs.get('unique_identifier')
            )

        _, loc_greeds_vals = self._connector.get_possible_greeds(
            unique_identifier=loc_kwargs.get('unique_identifier')
            )

        enemy_list = [en[0] for en in loc_enemies_vals]
        enemy_ratio_list = [en[1] for en in loc_enemies_vals]

        greed_list = [gr[0] for gr in loc_greeds_vals]
        greed_ratio_list = [gr[1] for gr in loc_greeds_vals]

        loc_kwargs['possible_enemies'] = enemy_list
        loc_kwargs['possible_enemies_ratio'] = enemy_ratio_list

        loc_kwargs['possible_greeds'] = greed_list
        loc_kwargs['possible_greeds_ratio'] = greed_ratio_list

        return Location(**loc_kwargs)
