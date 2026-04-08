import random
from .OutsiderClass import *

class Drunk(Outsider):
    def init(self):
        self.name = '酒鬼'


    def specInit(self, game):
        for i in range(0, len(game.identityAll['townsfolk'])):
            if game.identityAll['townsfolk'][i].used == 0:
                self.hasPretend = 1
                self.pretend = copy.deepcopy(game.identityAll['townsfolk'][i])
                self.pretend.seat = self.seat
                game.identityAll['townsfolk'][i].used = 1
                self.pretend.drunk.append('IsDrunk')
                # logger.info('我是' + str(self.seat) + '，我刚刚虚构了一个身份：' + self.pretend.name + '\n')
                break