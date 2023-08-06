from abstractgameunit import AbstractGameUnit


class OrcRider(AbstractGameUnit):
    def __init__(self):
        super().__init__()
        self.name = '兽人'
        self.max_hp = 30
        self.health_meter = 30
        self.unit_type = '敌军'

    def _info(self):
        print('很傻很天真')
