import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.minions.MinionClass import *

class EvilTwin(Minion):
    def init(self):
        self.name = '邪恶双子'
        # 黑夜来临前，视为恶魔。黑夜中，正常视为镜像双子
        self.firstPriority = 1
        self.priority = 1
        self.friend = 0
        self.back = 1

    def firstNight(self, game):

        if self.healthy == 1 and self.friend == 0:
            # 获取一个对立双子
            self.friend = self.seat
            cnt = 0
            while cnt < 1000 and game.players[self.friend].good == 0:
                cnt = cnt + 1
                self.friend = random.randint(1, game.playerNum[0])
            game.dayBoard[self.seat] += str(self.friend) + '是对立双子！ '
            game.dayBoard[self.friend] += str(self.seat) + '是对立双子！ '
            game.allBoard += str(self.seat) + '号邪恶双子连向了' + str(self.friend) + '\n'

        self.skill(game)
        return

    def night(self, game):
        self.skill(game)
        return

    def skill(self, game):
        if self.back == 0:
            if self.healthy != 0:
                if self.alive == 1 and game.players[self.friend].alive == 1:
                    self.back = 1
                    self.type = 'demon'
                    self.firstPriority = 1
                    self.priority = 1
                    return
        if self.back == 1:
            self.back = 0
            self.type = 'minion'
            self.firstPriority = 99
            self.priority = 99

            if self.healthy != 0:
                if self.alive == 1:
                    if game.lastDied == self.friend:
                        game.allBoard += str(self.seat) + '号是存活的镜像双子，而对立双子'\
                                                    + str(self.friend) + '号被处决\n'
                        game.allBoard += str(self.seat) + '号镜像双子触发了特殊胜利\n'
                        self.type = 'demon'
                        for i in range(1, game.playerNum[0] + 1):
                            if game.players[i].seat != self.seat:
                                game.players[i].killed(game)

