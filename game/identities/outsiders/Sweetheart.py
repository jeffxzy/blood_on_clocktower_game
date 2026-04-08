import random
from .OutsiderClass import *

class Sweetheart(Outsider):
    def init(self):
        self.name = '心上人'

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        # game.dayBoard[self.seat] += '❌'
        self.check()
        if self.healthy == 0:
            return
        cnt = 0
        while cnt < 1000:
            r = random.randint(1, game.playerNum[0])
            if game.players[r].good == 1 and r != self.seat:
                game.players[r].drunk.append(Status.SWEETHEART)
                game.allBoard += str(self.seat) + '号心上人醉了' + str(r) + '号\n'
                break