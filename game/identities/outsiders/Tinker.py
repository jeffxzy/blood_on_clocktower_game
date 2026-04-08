import random
from .OutsiderClass import *

class Tinker(Outsider):
    def init(self):
        self.name = '修补匠'
        self.priority = 48
        self.percent = 25
        
    def night(self, game):
        if self.alive == 1:
            if self.healthy == 1:
                if random.randint(1, 100) <= self.percent:
                    self.killed(game)
                    game.allBoard += str(self.seat) + '号修补匠死亡了\n'
                else:
                    self.percent = self.percent - 10