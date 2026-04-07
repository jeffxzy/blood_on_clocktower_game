import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class ClockMaker(Townsfolk):

    def init(self):
        self.name = '钟表匠'
        self.firstPriority = 40

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            r1, r2 = 1, 2
            # 避免死循环
            fin = 100
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'demon':
                    r1 = i
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'minion':
                    r2 = i
                    dis = max(r2 - r1, r1 - r2)
                    fin = min(fin, dis, game.playerNum[0] - dis)

            if self.healthy == 0:
                if random.randint(0, 1) == 0:
                    r = -1
                else:
                    r = 1
                fin = fin + r
                if fin <= 0:
                    fin = game.playerNum[0] / 2 - 2
                if fin > game.playerNum[0] / 2 - 1:
                    fin = 1
            fin = int(fin)

            game.dayBoard[self.seat] += '我得知' + str(fin)
            game.allBoard += str(self.seat) + '号钟表匠得知' + str(fin) + '\n'

        return
