import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Stargazer(Townsfolk):

    def init(self):
        self.name = '占星者'
        self.firstPriority = 40
        self.bad = 0

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:

            left = self.seat
            cnt = 0
            while cnt < 1000 and game.players[left].good != 0:
                cnt = cnt + 1
                left = left - 1
                if left < 1:
                    left = game.playerNum[0]
            right = self.seat
            cnt = 0
            while cnt < 1000 and game.players[right].good != 0:
                cnt = cnt + 1
                right = right + 1
                if right > game.playerNum[0]:
                    right = 1
            leftdis = max(self.seat - left, left - self.seat)
            leftfin = min(leftdis, game.playerNum[0] - leftdis)
            rightdis = max(self.seat - right, right - self.seat)
            rightfin = min(rightdis, game.playerNum[0] - rightdis)

            left = self.seat - 1
            if left < 1:
                left = game.playerNum[0]
            right = self.seat + 1
            if right > game.playerNum[0]:
                right = 1
            if game.players[left].good == 0 or game.players[right].good == 0:
                self.bad = 1

            # 如果周围有邪恶，并且自身不健康，获得正确信息
            if self.bad == 1 and self.healthy == 0:
                pass
            else:
                if self.bad == 1 or self.healthy == 0:
                    if leftfin < rightfin:
                        leftfin = rightfin + random.randint(0, 1)
                    elif leftfin > rightfin:
                        leftfin = rightfin - random.randint(0, 1)
                    elif leftfin == rightfin:
                        leftfin = rightfin + random.randint(0, 1) * 2 - 1

            # 注意！ left是序号更小的。
            if leftfin < rightfin:
                fin = '右侧（序号更小的方向）'
            if leftfin > rightfin:
                fin = '左侧（序号更大的方向）'
            if leftfin == rightfin:
                fin = '相同'

            game.dayBoard[self.seat] += '我得知' + str(fin)
            game.allBoard += str(self.seat) + '号占星者得知' + str(fin) + '\n'

        return
