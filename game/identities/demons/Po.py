import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class Po(Demon):
    def init(self):
        self.name = '珀'
        self.priority = 24
        self.waiting = 0

    def night(self, game):

        # 如果存活人数 <= 3，不憋刀
        a = 0
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].alive == 1:
                a = a + 1

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
                # 极特别的，剩余5人时尝试开三刀结束游戏
                if a == 5 and game.players[r3].alive == 1:
                    continue
                else:
                    break

        r = random.randint(1, 10)

        # 如果存活人数 <= 3，不憋刀
        if a <= 3:
            r = 10

        if self.healthy != 0 and self.alive == 1:
            if self.waiting == 0:
                if r <= 7:
                    game.allBoard += str(self.seat) + '号珀没有选择任何人\n'
                    self.waiting = 1
                else:
                    game.allBoard += str(self.seat) + '号珀杀死了' + str(r1) + '号\n'
                    game.players[r1].killed(game)
                    self.checkGrandmotherDeath(game, r1)
            else:
                game.allBoard += str(self.seat) + '号珀杀死了' + str(r1) + '号\n'
                game.allBoard += str(self.seat) + '号珀杀死了' + str(r2) + '号\n'
                game.allBoard += str(self.seat) + '号珀杀死了' + str(r3) + '号\n'
                game.players[r1].killed(game)
                self.checkGrandmotherDeath(game, r1)
                game.players[r2].killed(game)
                self.checkGrandmotherDeath(game, r2)
                game.players[r3].killed(game)
                self.checkGrandmotherDeath(game, r3)
                self.waiting = 0
    