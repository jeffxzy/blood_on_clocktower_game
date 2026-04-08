import random
from .MinionClass import *

class Assassin(Minion):

    def init(self):
        self.name = '刺客'
        self.priority = 37
        self.percent = 40
        self.skill = 1

    def night(self, game):
        # 查看是否还活着
        if self.alive == 1:
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1 and game.players[r1].good == 1:
                    break
            if self.healthy != 0 and self.skill == 1 and game.players[r1].type != 'demon':
                if random.randint(1, 100) <= self.percent:
                    self.skill = 0
                    game.allBoard += str(self.seat) + '号刺客杀死了' + str(r1) + '号\n'
                    game.players[r1].killed(game)
                else:
                    self.percent = self.percent + 25