import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class Leviathan(Demon):
    def init(self):
        self.name = '利维坦'
        self.firstPriority = 1
        self.priority = 1
        self.dayCount = 0
        self.killCount = 0

    def firstNight(self, game):
        self.skill(game)

    def night(self, game):
        self.skill(game)

    def skill(self, game):
        self.dayCount = self.dayCount + 1
        if self.healthy == 1 and self.alive == 1:

            end = 0
            if game.lastDied != 0 and game.players[game.lastDied].good == 1:
                self.killCount = self.killCount + 1
            if self.killCount >= 2:
                end = 1
                game.allBoard += str(self.seat) + '号为利维坦，且多于1名善良玩家被处决\n'
            if self.dayCount == 6:
                end = 1
                game.allBoard += str(self.seat) + '号为利维坦，且第5天结束\n'

            if end == 1:
                game.allBoard += str(self.seat) + '号利维坦杀死了其它所有玩家\n'
                for i in range(1, game.playerNum[0] + 1):
                    if i != self.seat:
                        game.players[i].killed(game)

            else:
                game.dayBoard[0] += '⚠利维坦在场⚠\n现在是第' + str(self.dayCount) + '天。\n'

