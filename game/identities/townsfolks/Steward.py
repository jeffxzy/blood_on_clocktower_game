import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *


class Steward(Townsfolk):

    def init(self):
        self.name = '事务官'
        self.firstPriority = 44

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            # 避免死循环
            cnt = 0
            see = 0
            while cnt < 1000:
                cnt = cnt + 1
                # 选取随机玩家
                r1 = random.randint(1, game.playerNum[0])
                if self.healthy:
                    if (game.players[r1].type == 'townsfolk' or game.players[r1].type == 'outsider') and r1 != self.seat:
                        see = r1
                        break
                if not self.healthy:
                    if (game.players[r1].type == 'minion' or game.players[r1].type == 'demon') and r1 != self.seat:
                        see = r1
                        break

            if see == 0:
                game.dayBoard[self.seat] += '我得知没有任何善良玩家在场。'
                game.allBoard += str(self.seat) + '号事务官得知没有善良玩家在场。\n'
            else:
                game.dayBoard[self.seat] += str(see)
                game.allBoard += str(self.seat) + '号事务官得知' + str(see) + '\n'

        return
