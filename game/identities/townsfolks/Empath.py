import random
from .TownsfolkClass import *

class Empath(Townsfolk):

    def init(self):
        self.name = '共情者'
        self.firstPriority = 36
        self.priority = 53

    def firstNight(self, game):
        self.skill(game)
        return

    def night(self, game):
        self.skill(game)
        return

    def skill(self, game):
        if self.alive == 1:
            fin = 0
            # 避免死循环
            left = self.seat
            cnt = 0
            while cnt < 1000 and (game.players[left].alive == 0 or left == self.seat):
                cnt = cnt + 1
                left = left - 1
                if left < 1:
                    left = game.playerNum[0]
            right = self.seat
            cnt = 0
            while cnt < 1000 and (game.players[right].alive == 0 or right == self.seat):
                cnt = cnt + 1
                right = right + 1
                if right > game.playerNum[0]:
                    right = 1

            if game.players[left].good == 0:
                fin = fin + 1
            if game.players[right].good == 0:
                fin = fin + 1

            if self.healthy == 0:
                fin = fin - 1
                if fin == -1:
                    fin = 1

            if left > right:
                left, right = right, left

            game.dayBoard[self.seat] += str(left) + '/' + str(right) + '得' + str(fin) + '  '
            game.allBoard += str(self.seat) + '号共情者得知' + str(left) + '/' + str(right) + '得' + str(fin) + '\n'