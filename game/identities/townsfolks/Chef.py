import random
from .TownsfolkClass import *

class Chef(Townsfolk):

    def init(self):
        self.name = '厨师'
        self.firstPriority = 35

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            fin = 0
            for i in range(1, game.playerNum[0]):
                if game.players[i].good == 0 and game.players[i + 1].good == 0:
                    fin = fin + 1
            if game.players[1].good == 0 and game.players[game.playerNum[0]].good == 0:
                    fin = fin + 1
            if self.healthy == 0:
                fin = fin - 1
            if fin == -1:
                fin = 1

            game.dayBoard[self.seat] += '我得知' + str(fin)
            game.allBoard += str(self.seat) + '号厨师得知' + str(fin) + '\n'

        return
