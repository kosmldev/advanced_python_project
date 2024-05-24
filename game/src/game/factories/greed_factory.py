import datetime
import hashlib
from random import getrandbits


from src.game.constructor.factories import BaseFactory
from src.game.connectors.greed_connector import GreedFactoryConnector
from src.game.subjects.greed import Greed
from src.game.subjects.location import Location


import numpy as np


class GreedFactory(BaseFactory):

    def __init__(self,
                 connector: GreedFactoryConnector = None,
                 **kwargs) -> None:
        super().__init__(
            connector=connector,
            **kwargs
            )

    def load_existed_greed(self,
                           unique_identifer: str = None) -> Greed:

        greed_info_cols, greed_info_values = self._connector.get_greed(
            unique_identifer
            )

        greed_info = {
            list(greed_info_cols)[i]: list(greed_info_values)[0][i]
            for i in range(len(list(greed_info_cols)))
            }

        return Greed(**greed_info)

    def create_random_new_greed(self,
                                loc: Location = None) -> Greed:
        possible_greeds, ratio = loc.get_possible_greeds()

        greed_name = np.random.choice(possible_greeds, size=1, p=ratio)[0]

        now_datetime = datetime.datetime.now()

        greed_info_cols, greed_info_values = self._connector.get_greed_info(
            start_dttm=now_datetime,
            end_dttm=now_datetime,
            name=greed_name
        )

        greed_info = {
            list(greed_info_cols)[i]: list(greed_info_values)[0][i]
            for i in range(len(list(greed_info_cols)))
            }

        random_hash = getrandbits(128)

        md5_unique_identifier = hashlib.md5(
            bytes(f"{now_datetime}_{random_hash}", encoding='utf-8')
            ).hexdigest()

        self._connector.push_new_greed(
            id=md5_unique_identifier,
            dttm_created=now_datetime,
            dttm_updated=now_datetime,
            update_identifier=greed_info.get('profit_type'),
            value=greed_info.get('profit')
        )

        self._connector.push_new_greed_link(
            base_id=greed_info.get('base_id'),
            greed_id=md5_unique_identifier,
            dttm=now_datetime
        )

        del greed_info['base_id']

        greed_kwargs = {
            'name': greed_name,
            'unique_identifier': md5_unique_identifier
        }

        return Greed(**{**greed_info, **greed_kwargs})
