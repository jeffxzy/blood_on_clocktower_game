import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Dreamer(Townsfolk):

    def init(self):
        self.name = '筑梦师'
        self.firstPriority = 41
        self.priority = 57
        self.got = []

    def firstNight(self, game):
        self.skill(game)
        return

    def night(self, game):
        self.skill(game)
        return

    def skill(self, game):
        if self.alive == 1:
            # 避免死循环
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and not r1 in self.got:
                    break

            cnt = 0
            name1 = game.players[r1].name

            if self.healthy == 0:
                # 邪恶的伪装：3/4概率给正确信息
                if 'isEvil' in self.poisoned and random.randint(1, 4) <= 3:
                    pass
                else:
                    if game.players[r1].good == 1:
                        while cnt < 1000:
                            cnt = cnt + 1
                            r = game.getRandomIdentity(game, '12')
                            if r.name != name1:
                                name1 = r.name
                                break
                    else:
                        while cnt < 1000:
                            cnt = cnt + 1
                            r = game.getRandomIdentity(game, '34')
                            if r.name != name1:
                                name1 = r.name
                                break

            name2 = ''
            if game.players[r1].good == 1:
                while cnt < 1000:
                    cnt = cnt + 1
                    r = game.getRandomIdentity(game, '34')
                    if r.name != name1:
                        name2 = r.name
                        break
            else:
                while cnt < 1000:
                    cnt = cnt + 1
                    r = game.getRandomIdentity(game, '12')
                    if r.name != name1:
                        name2 = r.name
                        break
                # 红有3/4概率给到伪装信息
                if random.randint(1, 4) <= 3:
                    if game.players[r1].hasPretend == 1:
                        name2 = game.players[r1].pretend.name
                name1, name2 = name2, name1

            game.dayBoard[self.seat] += str(r1) + name1 + '/' + name2 + ' '
            game.allBoard += str(self.seat) + '号筑梦得知' + str(r1) + name1 + '/' + name2 + '\n'
            self.got.append(r1)