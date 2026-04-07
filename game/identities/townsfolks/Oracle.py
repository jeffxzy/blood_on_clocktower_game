import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Oracle(Townsfolk):

    def init(self):
        self.name = '神谕者'
        self.priority = 60
        self.last = 0

    def night(self, game):
        # 查看是否还活着
        if self.alive == 1:
            cnt = 0
            for i in game.players:
                if i == 'nothing':
                    continue
                if i.alive == 0:
                    if i.good == 0:
                        cnt = cnt + 1
            if self.healthy == 0:
                cnt = cnt - 1
                if cnt < self.last or cnt < 0:
                    cnt = cnt + 2
                self.last = cnt
            game.dayBoard[self.seat] += '得知' + str(cnt) + ' '
            game.allBoard += str(self.seat) + '号神谕者得知' + str(cnt) + '\n'

        return
