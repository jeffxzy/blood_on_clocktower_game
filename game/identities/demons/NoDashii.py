import random
import os

from nonebot.log import logger
from .DemonClass import *

class NoDashii(Demon):
    def init(self):
        self.name = '诺·达颯'
        self.firstPriority = 1
        self.priority = 30

    def firstNight(self, game):
        left = self.seat
        cnt = 0
        while cnt < 1000 and game.players[left].type != 'townsfolk':
            cnt = cnt + 1
            left = left - 1
            if left < 1:
                left = game.playerNum[0]
        right = self.seat
        cnt = 0
        while cnt < 1000 and game.players[right].type != 'townsfolk':
            cnt = cnt + 1
            right = right + 1
            if right > game.playerNum[0]:
                right = 1
        game.players[left].poisoned.append('NoDashii')
        game.players[right].poisoned.append('NoDashii')
        game.allBoard += str(left) + '号和' + str(right) + '号因诺·达颯中毒\n'


    def night(self, game):
        cnt = 0
        r1 = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat and game.players[r1].alive == 1:
                break
        if self.healthy != 0 and self.alive == 1:
            game.players[r1].killed(game)
            game.allBoard += str(self.seat) + '号诺·达颯杀死了' + str(r1) + '号\n'
            self.checkGrandmotherDeath(game, r1)
    