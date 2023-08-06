from abc import ABCMeta, abstractmethod
from gameuniterror import HealthMeterException
from gameutils import *


class AbstractGameUnit(metaclass=ABCMeta):

    def __init__(self):
        self.name = None
        self.type = None
        self.max_hp = 0
        self.health_meter = 0
        self.unit_type = None

    @abstractmethod
    def _info(self):
        print(f'我是一个{self.name}')

    def heal(self, heal_by=10, full_healing=False):
        if self.health_meter == self.max_hp:
            print('你已满血')
            return

        if full_healing:
            self.health_meter = self.max_hp
            print('加满了')
        else:
            self.health_meter += heal_by
            print("好队友")
        if self.health_meter > self.max_hp:
            raise HealthMeterException('血量大于最大生命值了!')
        # max = a if a>b else b

    def reset_health_meter(self):
        """Reset the `health_meter` (assign default hit points)"""
        self.health_meter = self.max_hp

    def show_health(self, bold=True, end='\n'):

        msg = "Health: %s: %d" % (self.name, self.health_meter)

        if bold:
            print_bold(msg, end=end)
        else:
            print(msg, end=end)
