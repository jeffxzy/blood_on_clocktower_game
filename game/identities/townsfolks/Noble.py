import random
from .TownsfolkClass import *

class Noble(Townsfolk):

    def init(self):
        self.name = '贵族'
        self.firstPriority = 43

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            # 避免死循环

            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].good == 0:
                    break
            while cnt < 1000:
                cnt = cnt + 1
                r2 = random.randint(1, game.playerNum[0])
                if r2 != self.seat and r2 != r1 and game.players[r2].good == 1:
                    break
            while cnt < 1000:
                cnt = cnt + 1
                r3 = random.randint(1, game.playerNum[0])
                if r3 != self.seat and r3 != r1 and r3 != r2 and game.players[r3].good == 1:
                    break

            if self.healthy == 0:
                if random.randint(1, 3) <= 2:
                    while cnt < 1000:
                        cnt = cnt + 1
                        r1 = random.randint(1, game.playerNum[0])
                        if r1 != self.seat and r1 != r2 and r1 != r3 and game.players[r1].good == 1:
                            break
                else:
                    while cnt < 1000:
                        cnt = cnt + 1
                        r2 = random.randint(1, game.playerNum[0])
                        if r2 != self.seat and r2 != r1 and r2 != r3 and game.players[r2].good == 0:
                            break

            if r1 > r2:
                r1, r2 = r2, r1
            if r2 > r3:
                r2, r3 = r3, r2
            if r1 > r2:
                r1, r2 = r2, r1

            game.dayBoard[self.seat] += '我得知' + str(r1) + ' ' + str(r2) + ' ' + str(r3)
            game.allBoard += str(self.seat) + '号贵族得知' + str(r1) + ' ' + str(r2) + ' ' + str(r3) + '\n'

        return
