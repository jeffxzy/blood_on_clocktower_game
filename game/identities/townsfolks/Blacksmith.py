import random
from .TownsfolkClass import *


class Blacksmith(Townsfolk):

    def init(self):
        self.name = '铁匠'
        self.firstPriority = 34

    def firstNight(self, game):
        if self.alive == 1:
            outsiderCount = 0
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'outsider':
                    outsiderCount = outsiderCount + 1

            if self.healthy == 0:
                outsiderCount = random.randint(0, game.playerNum[2] + 2)

            game.dayBoard[self.seat] += '我得知有' + str(outsiderCount) + '名外来者在场。'
            game.allBoard += str(self.seat) + '号铁匠得知有' + str(outsiderCount) + '名外来者在场。\n'

        return

    def preFirstNight(self, game):
        self.check()
        self.updateOutsidersDrunk(game)
        return

    def preNight(self, game):
        self.check()
        self.updateOutsidersDrunk(game)
        return

    def updateOutsidersDrunk(self, game):
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].type == 'outsider':
                if self.alive == 1 and self.healthy == 1:
                    if Status.BLACKSMITH not in game.players[i].drunk:
                        game.players[i].drunk.append(Status.BLACKSMITH)
                        if game.players[i].hasPretend == 1:
                            game.players[i].pretend.drunk.append(Status.BLACKSMITH)
                else:
                    if Status.BLACKSMITH in game.players[i].drunk:
                        game.players[i].drunk.remove(Status.BLACKSMITH)
                        if game.players[i].hasPretend == 1:
                            if Status.BLACKSMITH in game.players[i].pretend.drunk:
                                game.players[i].pretend.drunk.remove(Status.BLACKSMITH)
        return

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        if self.hasPretend == 1:
            self.pretend.killed(game)
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].type == 'outsider':
                if Status.BLACKSMITH in game.players[i].drunk:
                    game.players[i].drunk.remove(Status.BLACKSMITH)
                    if game.players[i].hasPretend == 1:
                        if Status.BLACKSMITH in game.players[i].pretend.drunk:
                            game.players[i].pretend.drunk.remove(Status.BLACKSMITH)
        game.allBoard += str(self.seat) + '号铁匠死亡，外来者醉酒状态解除。\n'
        return

