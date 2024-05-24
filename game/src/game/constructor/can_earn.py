class CanEarn(object):

    def __init__(
            self,
            balance: int = None,
            experiance: int = None,
            mana: int = None,
            **kwargs) -> None:
        self._balance = balance
        self._experiance = experiance
        self._mana = mana

    def get_mana(self) -> int:
        return self._mana

    def get_balance(self) -> int:
        return self._balance

    def get_hp(self) -> int:
        return self._hp

    def get_experiance(self) -> int:
        return self._experiance

    def earn(
            self,
            profit: int = None,
            profit_type: str = None) -> None:
        if profit_type == 'money':
            self.upgrade_balance(profit)
        elif profit_type == 'experiance':
            self.upgrade_experiance(profit)
        elif profit_type == 'hp':
            self.upgrade_hp(profit)
        elif profit_type == 'mana':
            self.upgrade_mana(profit)
        elif profit_type == 'l_attack':
            self.upgrade_l_attack(profit)
        elif profit_type == 'u_attack':
            self.upgrade_u_attack(profit)
        else:
            # Add another activity here
            print('Unknown profit_type')
            raise ValueError

    def upgrade_balance(self, profit: int = None) -> None:
        self._balance += profit

    def upgrade_experiance(self, profit: int = None) -> None:
        self._experiance += profit

    def upgrade_hp(self, profit: int = None) -> None:
        self._hp += profit

    def upgrade_mana(self, profit: int = None) -> None:
        self._mana += profit

    def upgrade_l_attack(self, profit: int = None) -> None:
        self._attack_power_lower += profit

    def upgrade_u_attack(self, profit: int = None) -> None:
        self._attack_power_upper += profit
