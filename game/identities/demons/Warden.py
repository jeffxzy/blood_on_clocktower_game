import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class Warden(Demon):
    def init(self):
        self.name = '典狱长'
        self.firstPriority = 15
        self.priority = 25
        self.last = [-1, -1, -1]

    def firstNight(self, game):
        self.skill(game)
    def night(self, game):
        self.skill(game)

    def skill(self, game):

        if self.alive == 1:
            cnt = 0
            r1, r2, r3 = 0, 0, 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    break
            while cnt < 1000:
                cnt = cnt + 1
                r2 = random.randint(1, game.playerNum[0])
                if r2 != self.seat and game.players[r2].alive == 1 and r2 != r1:
                    break
            while cnt < 1000:
                cnt = cnt + 1
                r3 = random.randint(1, game.playerNum[0])
                if r3 != self.seat and r3 != r2 and r3 != r1:
                    break


            if self.healthy != 0:
                ok = 0
                if game.lastDied != 0:
                    for i in range(0, 3):
                        if game.lastDied == self.last[i]:
                            ok = 1
                            for j in range(0, 3):
                                game.players[self.last[j]].killed(game)
                                game.allBoard += str(self.seat) + '号典狱长杀死了' + str(self.last[j]) + '号\n'
                                self.checkGrandmotherDeath(game, self.last[j])
                if ok == 0 and game.days != 1:
                    i = self.last[random.randint(0, 2)]
                    game.players[i].killed(game)
                    game.allBoard += str(self.seat) + '号典狱长杀死了' + str(i) + '号\n'
                    self.checkGrandmotherDeath(game, i)

            self.last = [r1, r2, r3]
            game.allBoard += str(self.seat) + '号典狱长选择了' + str(r1) + '/' + str(r2) + '/' + str(r3) + '\n'