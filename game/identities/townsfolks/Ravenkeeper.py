import random
from .TownsfolkClass import *

class Ravenkeeper(Townsfolk):

    def init(self):
        self.name = '守鸦人'
        self.skill = 0
        self.priority = 42

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        # game.dayBoard[self.seat] += '❌'
        if game.status != 'night':
            return
        self.skill = 1
        return

    def night(self, game):
        if self.skill == 0:
            return
        self.skill = 0
        cnt = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat:
                fin = game.players[r1].name
                break
        if self.healthy == 0:
            # 邪恶的伪装：3/4概率给正确信息
            if Status.IS_EVIL in self.poisoned and random.randint(1, 4) <= 3:
                pass
            else:
                cnt = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r2 = random.randint(1, game.playerNum[0])
                    if r2 != self.seat and r2 != r1:
                        fin = game.players[r2].name

        game.dayBoard[self.seat] += '我得知' + str(r1) + '号是' + fin
        game.allBoard += str(self.seat) + '号守鸦人得知' + str(r1) + '号是' + fin + '\n'