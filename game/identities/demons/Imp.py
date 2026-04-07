import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class Imp(Demon):
    def init(self):
        self.name = '小恶魔'
        self.priority = 24

    def night(self, game):
        cnt = 0
        r1 = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat and game.players[r1].alive == 1:
                break


        if self.healthy != 0 and self.alive == 1:
            game.allBoard += str(self.seat) + '号小恶魔杀死了' + str(r1) + '号\n'
            game.players[r1].killed(game)
            self.checkGrandmotherDeath(game, r1)
    