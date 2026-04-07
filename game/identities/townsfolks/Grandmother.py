import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Grandmother(Townsfolk):

    def init(self):
        self.name = '祖母'
        self.firstPriority = 35
        self.grandchildSeat = 0
        self.firstNightHealthy = 1

    def specInit(self, game):
        self.firstNightHealthy = 1

    def firstNight(self, game):
        if self.alive == 0:
            return

        self.check()
        if self.healthy == 0:
            self.firstNightHealthy = 0

        cnt = 0
        realGrandchild = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat and game.players[r1].good == 1:
                realGrandchild = r1
                self.grandchildSeat = r1
                break

        showSeat = realGrandchild
        showName = ''

        if game.players[realGrandchild].name == '酒鬼':
            showName = '酒鬼'
        elif game.players[realGrandchild].hasPretend == 1:
            showName = game.players[realGrandchild].pretend.name
        else:
            showName = game.players[realGrandchild].name

        if self.firstNightHealthy == 0 or 'isEvil' in self.poisoned:
            r = random.randint(1, 100)
            if r <= 80:
                cnt = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r1 = random.randint(1, game.playerNum[0])
                    if r1 != self.seat and game.players[r1].good == 0:
                        showSeat = r1
                        if game.players[r1].name == '酒鬼':
                            showName = '酒鬼'
                        elif game.players[r1].hasPretend == 1:
                            showName = game.players[r1].pretend.name
                        else:
                            showName = game.players[r1].name
                        break
            elif r <= 90:
                cnt = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r1 = random.randint(1, game.playerNum[0])
                    if r1 != self.seat:
                        showSeat = r1
                        showName = '酒鬼'
                        break
            else:
                cnt = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r1 = random.randint(1, game.playerNum[0])
                    if r1 != self.seat:
                        showSeat = r1
                        if game.players[r1].name == '酒鬼':
                            showName = '酒鬼'
                        elif game.players[r1].hasPretend == 1:
                            showName = game.players[r1].pretend.name
                        else:
                            showName = game.players[r1].name
                        break

        game.dayBoard[self.seat] += str(showSeat) + '号玩家是你的孙子，他是' + showName
        game.allBoard += str(self.seat) + '号祖母得知' + str(showSeat) + '号是他的孙子，他是' + showName + '\n'

    def checkGrandchildDeath(self, game, killedSeat, killedByDemon):
        if self.alive == 0:
            return
        if killedSeat != self.grandchildSeat:
            return
        if not killedByDemon:
            return

        self.check()
        if self.healthy == 0 or self.firstNightHealthy == 0:
            return

        isSpy = hasattr(game.players[killedSeat], 'back')
        
        if isSpy:
            r = random.randint(1, 100)
            if r <= 70:
                game.allBoard += str(self.seat) + '号祖母因孙子' + str(killedSeat) + '号（间谍）被恶魔杀死而一同死亡\n'
                self.killed(game)
            else:
                game.allBoard += str(self.seat) + '号祖母的孙子' + str(killedSeat) + '号（间谍）被恶魔杀死，但祖母侥幸存活\n'
        else:
            game.allBoard += str(self.seat) + '号祖母因孙子' + str(killedSeat) + '号被恶魔杀死而一同死亡\n'
            self.killed(game)
