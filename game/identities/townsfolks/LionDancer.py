import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class LionDancer(Townsfolk):

    def init(self):
        self.name = '舞狮人'
        self.priority = 60
        self.got = []

    def night(self, game):
        # 查看是否还活着
        if self.alive == 1:
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                i = game.getRandomIdentity(game, '1234')

                # 避免拿到重复身份
                if i.name in self.got:
                    continue


                found = 0
                for j in range(1, game.playerNum[0] + 1):
                    if i.name == game.players[j].name:
                        found = 1

                evilR = random.randint(1, 3)

                if found == 1:
                    if self.healthy == 1 or ('isEvil' in self.poisoned and evilR <= 2):
                        game.dayBoard[self.seat] += '得知' + i.name + ' '
                        game.allBoard += str(self.seat) + '号舞狮人得知' + i.name + '\n'
                        self.got.append(i.name)
                        return
                elif found == 0:
                    if self.healthy == 0 and (not 'isEvil' in self.poisoned or evilR > 3):
                        game.dayBoard[self.seat] += '得知' + i.name + ' '
                        game.allBoard += str(self.seat) + '号舞狮人得知' + i.name + '\n'
                        self.got.append(i.name)
                        return

        return
