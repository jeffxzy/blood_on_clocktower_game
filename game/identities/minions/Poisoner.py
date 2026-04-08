import random
from .MinionClass import *

class Poisoner(Minion):

    def init(self):
        self.name = '投毒者'
        self.firstPriority = 8
        self.priority = 17
    
    def firstNight(self, game):
        # do sth to pretend I'm good

        # 检查存活
        if self.alive == 1:
            # 避免死循环
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                # 检查坏状态
                if self.healthy == 0:
                    return
                r1 = random.randint(1, game.playerNum[0])
                if game.players[r1].good == 1 and game.players[r1].alive == 1:
                    if game.players[r1].hasPretend == 1:
                        game.players[r1].pretend.poisoned.append(Status.POISONER)
                    else:
                        game.players[r1].poisoned.append(Status.POISONER)
                    game.allBoard += str(self.seat) + '号投毒者毒了' + str(r1) + '\n'
                    return

    def night(self, game):
        # 检查存活
        if self.alive == 1:
            # 避免死循环
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                # 检查坏状态
                if self.healthy == 0:
                    return
                r1 = random.randint(1, game.playerNum[0])
                if game.players[r1].good == 1 and game.players[r1].alive == 1:
                    if game.players[r1].hasPretend == 1:
                        game.players[r1].pretend.poisoned.append(Status.POISONER)
                    else:
                        game.players[r1].poisoned.append(Status.POISONER)
                    game.allBoard += str(self.seat) + '号投毒者毒了' + str(r1) + '\n'
                    return

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        if self.hasPretend == 1:
            self.pretend.killed(game)
        for i in range(1, game.playerNum[0] + 1):
            if Status.POISONER in game.players[i].poisoned:
                game.players[i].poisoned.remove(Status.POISONER)
                game.allBoard += str(i) + '号因投毒者的中毒消除了\n'

