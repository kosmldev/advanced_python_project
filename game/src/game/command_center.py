from datetime import datetime
import os

import numpy as np

# from .enemy import Enemy
# from .user import User
# from .location import Location
# from .greed import Greed
# from .battlefield import Battlefield

from src.game.connectors.user_connector import (
    UserFactoryConnectorBaseInfo,
    UserFactoryConnectorUpdater
)
from src.game.connectors.enemy_connector import EnemyFactoryConnector
from src.game.connectors.greed_connector import GreedFactoryConnector
from src.game.connectors.battlefield_connector import (
    BattlefieldActionConnector
)
from src.game.connectors.greedfield_connector import GreedfieldActionConnector
from src.game.connectors.location_connector import LocationFactoryConnector
from src.game.connectors.command_center_connector import CommandCenterConnector
from src.game.factories.user_factory import (
    UserFactoryBaseInfo,
    UserFactoryUpdater
)
from src.game.factories.enemy_factory import EnemyFactory
from src.game.factories.greed_factory import GreedFactory
from src.game.factories.battlefield_factory import BattlefieldFactory
from src.game.factories.greedfield_factory import GreedfieldFactory
from src.game.factories.location_factory import LocationFactory


DATABASE_CONGIF = {
    "username": os.getenv("DB__USERNAME"),
    "password": os.getenv("DB__PASSWORD"),
    "host": os.getenv("DB__HOST"),
    "port": os.getenv("DB__PORT"),
    "database": os.getenv("DB__DATABASE"),
    "connection_type": os.getenv("DB__TYPE")
}
print(DATABASE_CONGIF)


class CommandCenter:
    def __init__(self) -> None:
        self._start_dttm = datetime.now()
        self._current_state = 0

        self._command_conn = CommandCenterConnector(**DATABASE_CONGIF)
        self._user_base_conn = UserFactoryConnectorBaseInfo(**DATABASE_CONGIF)
        self._user_upd_conn = UserFactoryConnectorUpdater(**DATABASE_CONGIF)
        self._enemy_conn = EnemyFactoryConnector(**DATABASE_CONGIF)
        self._greed_conn = GreedFactoryConnector(**DATABASE_CONGIF)
        self._loc_conn = LocationFactoryConnector(**DATABASE_CONGIF)
        self._bat_conn = BattlefieldActionConnector(**DATABASE_CONGIF)
        self._grf_conn = GreedfieldActionConnector(**DATABASE_CONGIF)

        self._user_base_fact = UserFactoryBaseInfo(self._user_base_conn)
        self._user_upd_fact = UserFactoryUpdater(self._user_upd_conn)
        self._enemy_fact = EnemyFactory(self._enemy_conn)
        self._greed_fact = GreedFactory(self._greed_conn)
        self._loc_fact = LocationFactory(self._loc_conn)
        self._bat_fact = BattlefieldFactory(self._bat_conn)
        self._grf_fact = GreedfieldFactory(self._grf_conn)

        self._current_user = None
        self._current_enemy = None
        self._current_loc = None
        self._current_greed = None
        self._current_battlefield = None
        self._current_greedfield = None

        _, av_com_vals = self._command_conn.load_commands(
            current_dttm=self._start_dttm
        )

        self._commands_dict = {}
        self._available_commands = []

        for one_command in av_com_vals:
            self._commands_dict[one_command[0]] = {
                'descr': one_command[1],
                'attributes': []
            }
            self._available_commands.append(one_command[0])

            _, atr_com_vals = self._command_conn.load_comman_descr(
                command=one_command[0],
                current_dttm=self._start_dttm
            )

            if atr_com_vals:
                for one_atr in atr_com_vals:
                    self._commands_dict[one_command[0]]['attributes'].append(
                        {
                            'name': one_atr[0],
                            'descr': one_atr[1]
                        }
                    )

        _, av_state_vals = self._command_conn.load_states(
            current_dttm=self._start_dttm
        )

        self._states_dict = {}

        for one_state in av_state_vals:
            self._states_dict[one_state[0]] = one_state[1]

    def move(self) -> None:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        event = np.random.choice([2, 4], size=1, p=[0.5, 0.5])[0]

        self._current_user.update_state(event)
        self._user_upd_fact.update_state(
            user=self._current_user
        )
        self._current_state = self._current_user.get_state()

        if event == 2:
            self._current_enemy = self._enemy_fact.create_random_new_enemy(
                loc=self._current_loc
            )
            self._current_battlefield = self._bat_fact.create_battlefield(
                user=self._current_user,
                enemy=self._current_enemy,
                user_updater=self._user_upd_fact,
                enemy_updater=self._enemy_fact
            )
            out_message += 'На вашем пути встретился враг'
            out_message += f'\nИмя: {self._current_enemy.get_name()}'
            out_message += f'\nЗдоровье: {self._current_enemy.get_hp()}'
            out_message += '\nСила атаки: '
            out_message += f'{self._current_enemy.get_attack_power_lower()} - '
            out_message += f'{self._current_enemy.get_attack_power_upper()}'

        if event == 4:
            self._current_greed = self._greed_fact.create_random_new_greed(
                loc=self._current_loc
            )
            self._current_greedfield = self._grf_fact.create_greedfield(
                user=self._current_user,
                greed=self._current_greed,
                user_updater=self._user_upd_fact,
                greed_updater=self._greed_fact
            )
            out_message += 'На вашем пути встретилась плюшка'
            out_message += f'\nИмя: {self._current_greed.get_name()}'
            out_message += '\nТип бонуса: '
            out_message += f'{self._current_greed.get_profit_type()}'
            out_message += '\nБонус: '
            out_message += f'{self._current_greed.get_profit()}'

        return out_message

    def attack(self) -> str:
        out_message = '\n\n'
        if self._current_state != 3:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        cont = self._current_battlefield.make_turn()

        self._current_user = self._current_battlefield.get_user()
        self._current_enemy = self._current_battlefield.get_enemy()
        en_hp = self._current_enemy.get_hp()
        us_hp = self._current_user.get_hp()

        out_message += f'Ваше здоровье - {us_hp}'
        self._user_upd_fact.update_hp(
            user=self._current_user
        )
        self._enemy_fact.update_hp(
            enemy=self._current_enemy
        )

        if not cont:
            out_message += '\nБой закончен! С победой!'
            self._bat_fact.end_battlefield(
                battlefield=self._current_battlefield
            )
            self._enemy_fact.update_dead(
                enemy=self._current_enemy
            )

            u_atck = self._current_enemy.get_attack_power_upper()
            l_atck = self._current_enemy.get_attack_power_lower()
            new_exp = u_atck + l_atck
            self._current_user.earn(
                profit=new_exp,
                profit_type='experiance'
            )
            out_message += f'\nПолучен опыт - {new_exp}'
            self._user_upd_fact.update_experiance(
                user=self._current_user
            )

            self._current_battlefield = None
            self._current_enemy = None
            self._current_user.update_state(
                state=1
            )
            self._user_upd_fact.update_state(
                user=self._current_user
            )
            self._current_state = self._current_user.get_state()
            return out_message

        out_message += f'\nЗдоровье соперника - {en_hp}'
        return out_message

    def take(self) -> str:
        out_message = '\n\n'
        if self._current_state != 4:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        out_message += 'Бонус получен!'
        self._current_greedfield.take_greed()
        self._current_user = self._current_greedfield.get_user()
        self._grf_fact.end_greedfield(
            greedfield=self._current_greedfield
        )
        self._user_upd_fact.update_balance(
            user=self._current_user
        )
        self._user_upd_fact.update_hp(
            user=self._current_user
        )
        self._user_upd_fact.update_experiance(
            user=self._current_user
        )
        self._user_upd_fact.update_mana(
            user=self._current_user
        )
        self._user_upd_fact.update_attack(
            user=self._current_user
        )
        self._current_greedfield = None
        self._current_greed = None
        self._current_user.update_state(
            state=1
        )
        self._user_upd_fact.update_state(
            user=self._current_user
        )
        self._current_state = self._current_user.get_state()

        return out_message

    def skip(self) -> str:
        out_message = '\n\n'
        if self._current_state != 4:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        out_message += 'Бонус скипнут!'
        self._current_user = self._current_greedfield.get_user()
        self._grf_fact.end_greedfield(
            greedfield=self._current_greedfield
        )
        self._current_greedfield = None
        self._current_greed = None
        self._current_user.update_state(
            state=1
        )
        self._user_upd_fact.update_state(
            user=self._current_user
        )
        self._current_state = self._current_user.get_state()

        return out_message

    def trigger_wrong(self) -> str:
        out_message = '\n\n'
        out_message += 'Неверная команда'
        out_message += '\n'
        out_message += 'Воспользуйтесь /help для получения \
            информации по командам'

        return out_message

    def trigger_wrong_args(self) -> str:
        out_message = '\n\n'
        out_message += 'Неверные аргументы'
        out_message += '\n'
        out_message += 'Воспользуйтесь /help для получения \
            информации по командам'

        return out_message

    def help(self) -> str:
        out_message = '\n\n'
        out_message += 'Достпуные команды:'
        out_message += '\n\n'
        for one_key in self._commands_dict:
            descr = self._commands_dict.get(one_key).get('descr')
            out_message += f'\nКоманда: {one_key}, описание команды: {descr}'
            if self._commands_dict.get(one_key).get('attributes'):
                out_message += '\nВозможные атрибуты:'
                for one_attr in self._commands_dict.get(
                    one_key
                ).get('attributes'):
                    atr = one_attr.get('name')
                    atr_descr = one_attr.get('descr')
                    out_message += f'\nАтрибут: {atr}, описание: {atr_descr}'
            out_message += '\n'
        out_message += '\n\n'
        out_message += '--------------------------'

        return out_message

    def verbose(self) -> str:
        out_message = '\n\n'
        out_message += 'Ваше текущее состояние:'
        out_message += f'\n{self._states_dict.get(self._current_state)}'
        out_message += '\n\n'
        out_message += '--------------------------'
        out_message += '\n\n'

        if self._current_user is not None:
            out_message += 'Информация о пользователе:'
            out_message += f'\n{self._current_user.verbose()}'
            out_message += '\n\n'
            out_message += '--------------------------'
            out_message += '\n\n'

        if self._current_loc is not None:
            out_message += 'Информация о текущей локации:'
            out_message += f'\n{self._current_loc.verbose()}'
            out_message += '\n\n'
            out_message += '--------------------------'
            out_message += '\n\n'

        if self._current_greed is not None:
            out_message += 'Информация о награде:'
            out_message += f'\n{self._current_greed.verbose()}'
            out_message += '\n\n'
            out_message += '--------------------------'
            out_message += '\n\n'

        if self._current_enemy is not None:
            out_message += 'Информация о противнике:'
            out_message += f'\n{self._current_enemy.verbose()}'
            out_message += '\n\n'
            out_message += '--------------------------'
            out_message += '\n\n'

        return out_message

    def log(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 0:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        if not result_dict.get(
            '--username'
        ) or not result_dict.get('--password'):
            out_message = self.trigger_wrong_args()
            return out_message

        username = result_dict.get('--username')
        password = result_dict.get('--password')

        self._current_user = self._user_base_fact.load_user(
            username=username,
            password=password
        )
        self._current_loc = self._loc_fact.create_location(
            name=self._current_user._loc
        )
        self._current_user.move_to(
            loc=self._current_loc
        )
        self._current_state = self._current_user.get_state()

        if self._current_state in (2, 3):
            self._current_battlefield = self._bat_fact.load_battlefield(
                user=self._current_user,
                user_updater=self._user_upd_fact,
                enemy_updater=self._enemy_fact
            )
            self._current_enemy = self._current_battlefield.get_enemy()

        if self._current_state == 4:
            self._current_greedfield = self._grf_fact.load_greedfield(
                user=self._current_user,
                user_updater=self._user_upd_fact,
                greed_updater=self._greed_fact
            )
            self._current_greed = self._current_greedfield.get_greed()

        out_message += f"Пользователь {username} авторизован!"

        return out_message

    def new(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 0:
            out_message += 'В данном состоянии невозможно \
                выполнить данную команду'
            return out_message

        if not result_dict.get(
            '--username'
        ) or not result_dict.get('--password'):
            out_message = self.trigger_wrong_args()
            return out_message

        username = result_dict.get('--username')
        password = result_dict.get('--password')

        self._user_base_fact.create_new_user(
            username=username,
            password=password
        )
        out_message += f"Пользователь {username} создан!"

        return out_message

    def logout(self) -> str:
        self._current_user = None
        self._current_enemy = None
        self._current_loc = None
        self._current_greed = None
        self._current_battlefield = None
        self._current_greedfield = None
        self._current_state = 0
        out_message = ''
        out_message += 'Успешно разлогинены!'

        return out_message

    def chname(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно изменить имя'
            return out_message

        if result_dict.get('--new') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        self._user_upd_fact.update_username(
            user=self._current_user,
            new_name=result_dict.get('--new')
        )

        self._current_user.update_name(
            new_name=result_dict.get('--new')
        )

        out_message += 'Имя пользователя успешно изменено!'

        return out_message

    def chpass(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно изменить пароль'
            return out_message

        if result_dict.get(
            '--new'
        ) is None or result_dict.get('--old') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        self._user_upd_fact.update_password(
            user=self._current_user,
            old_pass=result_dict.get('--old'),
            new_pass=result_dict.get('--new')
        )

        out_message += 'Пароль успешно изменен!'

        return out_message

    def up_hp(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно увеличить hp'
            return out_message

        if result_dict.get('--value') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        result = self._current_user.up_hp(
            add=int(result_dict.get('--value'))
        )

        if result:
            self._user_upd_fact.update_experiance(
                user=self._current_user
            )
            self._user_upd_fact.update_hp(
                user=self._current_user
            )
            out_message += 'Обновление успешно завершено'
        else:
            out_message += 'Обновление на данное количество невозможно'

        return out_message

    def up_mana(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно увеличить mana'
            return out_message

        if result_dict.get('--value') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        result = self._current_user.up_mana(
            add=int(result_dict.get('--value'))
        )

        if result:
            self._user_upd_fact.update_experiance(
                user=self._current_user
            )
            self._user_upd_fact.update_mana(
                user=self._current_user
            )
            out_message += 'Обновление успешно завершено'
        else:
            out_message += 'Обновление на данное количество невозможно'

        return out_message

    def up_atck(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно увеличить hp'
            return out_message

        if result_dict.get(
            '--value'
        ) is None or result_dict.get('--which') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        result = self._current_user.up_attack(
            add=int(result_dict.get('--value')),
            which=result_dict.get('--which')
        )

        if result:
            self._user_upd_fact.update_experiance(
                user=self._current_user
            )
            self._user_upd_fact.update_hp(
                user=self._current_user
            )
            out_message += 'Обновление успешно завершено'
        else:
            out_message += 'Обновление на данное количество невозможно'

        return out_message

    def accept(self) -> str:
        out_message = '\n\n'
        if self._current_state != 2:
            out_message += 'В данном состоянии невозможно выполнить команду'
            return out_message
        self._current_user.update_state(
            state=3
        )
        self._current_state = self._current_user.get_state()
        self._user_upd_fact.update_state(
            user=self._current_user
        )
        out_message += 'Сражение принято!'

        return out_message

    def abandon(self) -> str:
        out_message = '\n\n'
        if self._current_state not in (2, 3):
            out_message += 'В данном состоянии невозможно выполнить команду'
            return out_message

        if self._current_state == 2:
            out_message += 'Вы как трус сбежали от новой драки'

        if self._current_state == 3:
            out_message += 'Сбежать с поля боя?!'
            out_message += '\nКринж..'

        exp = self._current_user.get_experiance()
        u_atck = self._current_enemy.get_attack_power_upper()

        if u_atck > exp:
            self._current_user.earn(
                profit=-exp,
                profit_type='experiance'
            )
        else:
            self._current_user.earn(
                profit=-u_atck,
                profit_type='experiance'
            )

        self._user_upd_fact.update_experiance(
            user=self._current_user
        )

        self._bat_fact.end_battlefield(
            battlefield=self._current_battlefield
        )

        self._current_enemy = None
        self._current_battlefield = None

        self._current_user.update_state(
            state=1
        )

        self._current_state = self._current_user.get_state()
        self._user_upd_fact.update_state(
            user=self._current_user
        )

        return out_message

    def moveto(self, result_dict: dict = None) -> str:
        out_message = '\n\n'
        if self._current_state != 1:
            out_message += 'В данном состоянии невозможно выполнить команду'
            return out_message

        if result_dict.get('--location') is None:
            out_message = self.trigger_wrong_args()
            return out_message

        self._current_loc = self._loc_fact.create_location(
            name=result_dict.get('--location')
        )

        self._current_user.move_to(
            loc=self._current_loc
        )

        self._user_upd_fact.update_location(
            user=self._current_user
        )

        out_message += 'Вы успешно переместились в '
        out_message += f"{result_dict.get('--location')}"

        return out_message

    def parse_log(self, log: str = None) -> str:

        parts = log.split()
        result_dict = {}

        current_key = None
        current_value = None

        for part in parts:
            if part.startswith("/"):
                result_dict['command'] = part
            if part.startswith("--"):
                if current_key is not None:
                    result_dict[current_key] = current_value.replace("'", "")
                current_key = part[:].replace("'", "")
                current_value = None
            else:
                if current_value is None:
                    current_value = part.replace("'", "")
                else:
                    current_value += " " + part.replace("'", "")

        if current_key is not None:
            result_dict[current_key] = current_value

        if result_dict.get("command") not in self._available_commands:
            answer = self.trigger_wrong()
            return answer

        if result_dict.get('command') == '/help':
            answer = self.help()
            return answer

        if result_dict.get("command") == '/new':
            answer = self.new(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/log':
            answer = self.log(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/verbose':
            answer = self.verbose()
            return answer

        if result_dict.get("command") == '/move':
            answer = self.move()
            return answer

        if result_dict.get("command") == '/moveto':
            answer = self.moveto(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/attack':
            answer = self.attack()
            return answer

        if result_dict.get("command") == '/take':
            answer = self.take()
            return answer

        if result_dict.get("command") == '/skip':
            answer = self.skip()
            return answer

        if result_dict.get("command") == '/logout':
            answer = self.logout()
            return answer

        if result_dict.get("command") == '/chname':
            answer = self.chname(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/chpass':
            answer = self.chpass(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/abandon':
            answer = self.abandon()
            return answer

        if result_dict.get("command") == '/accept':
            answer = self.accept()
            return answer

        if result_dict.get("command") == '/up_atck':
            answer = self.up_atck(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/up_hp':
            answer = self.up_hp(result_dict=result_dict)
            return answer

        if result_dict.get("command") == '/up_mana':
            answer = self.up_mana(result_dict=result_dict)
            return answer
