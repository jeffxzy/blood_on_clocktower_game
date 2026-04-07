import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class FortuneTeller(Townsfolk):

    def __init__(self):
        super().__init__()
        self.enemy = None

    def init(self):
        self.name = '占卜师'
        self.firstPriority = 37
        self.priority = 54

    def firstNight(self, game):
        cnt = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if game.players[r1].good == 1:
                self.enemy = r1
                break
        game.allBoard += str(self.seat) + '号占卜师的宿敌是' + str(self.enemy) + '\n'
        self.skill(game)
        return

    def night(self, game):
        self.skill(game)
        return

    def skill(self, game):
        if self.alive == 1:
            fin = '有'
            # 避免死循环
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                break
            while cnt < 1000:
                cnt = cnt + 1
                r2 = random.randint(1, game.playerNum[0])
                if r2 != r1:
                    break
            if game.players[r1].type == 'demon' or game.players[r2].type == 'demon' or \
                r1 == self.enemy or r2 == self.enemy:
                fin = '有'
            else:
                fin = '无'

            if self.healthy == 0:
                # 邪恶的伪装：2/3概率给正确信息
                if 'isEvil' in self.poisoned and random.randint(1, 3) <= 2:
                    pass
                else:


                    # 简单的反转信息
                    # if game.players[r1].type == 'demon' or game.players[r2].type == 'demon':
                    if fin == '有':
                        fin = '无'
                    else:
                        fin = '有'
            
            if r1 > r2:
                r1, r2 = r2, r1

            game.dayBoard[self.seat] += str(r1) + '/' + str(r2) + fin + '  '
            game.allBoard += str(self.seat) + '号占卜师得知' + str(r1) + '/' + str(r2) + fin + '\n'