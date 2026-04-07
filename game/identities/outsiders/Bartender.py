import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.outsiders.OutsiderClass import *

class Bartender(Outsider):
    def init(self):
        self.name = '酒保'
        self.firstPriority = 1

    def firstNight(self, game):
        if self.healthy == 1 and self.alive == 1:
            left = self.seat
            cnt = 0
            while cnt < 1000 and (game.players[left].good != 1 or left == self.seat):
                cnt = cnt + 1
                left = left - 1
                if left < 1:
                    left = game.playerNum[0]
            right = self.seat
            cnt = 0
            while cnt < 1000 and (game.players[right].good != 1 or right == self.seat):
                cnt = cnt + 1
                right = right + 1
                if right > game.playerNum[0]:
                    right = 1
            if random.randint(0, 1) == 0:
                game.players[left].drunk.append('bartender')
                game.allBoard += str(self.seat) + '号酒保醉了' + str(left) + '号\n'
            else:
                game.players[right].drunk.append('bartender')
                game.allBoard += str(self.seat) + '号酒保醉了' + str(right) + '号\n'