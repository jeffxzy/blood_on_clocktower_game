import random
from .TownsfolkClass import *

import copy

class Philosopher(Townsfolk):

    def init(self):
        self.name = '哲学家'
        self.firstPriority = 2
        self.priority = 2
        self.learnedIdentityName = ''

    def firstNight(self, game):
        if self.alive == 1:
            r = self.seat
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r = random.randint(1, len(game.identityAll['townsfolk']) - 1)
                if game.identityAll['townsfolk'][r].name != '哲学家':
                    break

            self.hasPretend = 1
            self.pretend = copy.deepcopy(game.identityAll['townsfolk'][r])
            self.pretend.check()
            self.pretend.init()
            self.pretend.seat = self.seat
            self.learnedIdentityName = self.pretend.name

            game.dayBoard[self.seat] += self.pretend.name + ' '
            game.allBoard += str(self.seat) + '号哲学家学习了' + self.pretend.name + '\n'

            if self.healthy == 0:
                self.pretend.drunk.append(Status.LEARN_FAILED)
            else:
                for i in range(1, game.playerNum[0] + 1):
                    if game.players[i].name == self.learnedIdentityName:
                        game.players[i].drunk.append(Status.PHILOSOPHER)
                        game.allBoard += str(i) + '号因哲学家而醉酒。\n'
        return

    def preFirstNight(self, game):
        self.check()
        self.checkLearnedIdentityDrunk(game)
        return

    def preNight(self, game):
        self.check()
        self.checkLearnedIdentityDrunk(game)
        return

    def checkLearnedIdentityDrunk(self, game):
        if self.learnedIdentityName == '':
            return
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].name == self.learnedIdentityName:
                if self.healthy == 0 or self.alive == 0:
                    if Status.PHILOSOPHER in game.players[i].drunk:
                        game.players[i].drunk.remove(Status.PHILOSOPHER)
                        game.allBoard += str(i) + '号因哲学家的醉酒消除了。\n'
                else:
                    if Status.PHILOSOPHER not in game.players[i].drunk:
                        game.players[i].drunk.append(Status.PHILOSOPHER)
                        game.allBoard += str(i) + '号因哲学家而醉酒。\n'
        return

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        if self.hasPretend == 1:
            self.pretend.killed(game)
        for i in range(1, game.playerNum[0] + 1):
            if self.learnedIdentityName != '' and game.players[i].name == self.learnedIdentityName:
                if 'philosopher' in game.players[i].drunk:
                    game.players[i].drunk.remove('philosopher')
                    game.allBoard += str(i) + '号因哲学家的醉酒消除了。\n'
