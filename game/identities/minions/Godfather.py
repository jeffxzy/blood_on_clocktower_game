import random
from .MinionClass import *

class Godfather(Minion):

    def init(self):
        self.name = '教父'
        self.priority = 38

    def night(self, game):
        # 查看是否还活着
        if self.alive == 1:
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1 and game.players[r1].type != 'demon':
                    break
            if self.healthy != 0 and game.lastDied != 0 and game.players[game.lastDied].type == 'outsider':
                game.players[r1].killed(game)
                game.allBoard += str(self.seat) + '号教父杀死了' + str(r1) + '号\n'