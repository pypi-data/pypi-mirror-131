from abstractgameunit import AbstractGameUnit
from gameutils import *
import random
class Knight(AbstractGameUnit):
    def __init__(self, name='权哥'):
        super(Knight, self).__init__()
        super().__init__()
        self.name = name
        self.max_hp = 100
        self.health_meter = 100
        self.unit_type = '友军'

    def _info(self):
        print(f'断剑重铸之日，骑士归来之时')

    def attack(self, enemy):
        # print('开始打架')
        # continue_attack = 'y'
        while (self.health_meter * enemy.health_meter) > 0:

            continue_attack = input('开始攻击？（y/n）:' or 'y')

            if continue_attack == 'n':

                print('跑路了')
                break

            elif continue_attack == 'y':
                injured_unit = random.choice([self, enemy])
                injury = random.randint(10, 15)
                print_bold(f'{self.name}血量为：{self.health_meter}{enemy.name}血量为：{enemy.health_meter}')
                injured_unit.health_meter = max(injured_unit.health_meter - injury, 0)
                print(f'开始战斗,{injured_unit.name}受到{injury}点伤害,血量是{injured_unit.health_meter}！')
            # else:
            #     print('请输入y/n')

            if self.health_meter <= 0:
                print('你没血了')
                break
            elif enemy.health_meter <= 0:
                print('你干掉了对方')
                break
                # self.attack(self,enemy)
