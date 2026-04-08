import random
from .OutsiderClass import *

class Recluse(Outsider):
    def init(self):
        self.name = '陌客'
        # 大多数邪恶行动完之后再判定
        self.firstPriority = 29
        self.priority = 39
        self.back = 0

    def firstNight(self, game):
        self.skill(game)
        return

    def night(self, game):
        self.skill(game)
        return

    def skill(self, game):
        if self.back == 0:
            if self.healthy != 0:
                r = random.randint(1, 10)
                if r <= 3:
                    self.back = 1
                    ide = game.getRandomIdentity(game, '34')
                    self.name = ide.name
                    self.type = ide.type
                    self.good = 0
                    self.firstPriority = 79
                    self.priority = 79
                    game.allBoard += str(self.seat) + '号陌客今晚接下来被视作' + self.name + '\n'
                    return
        if self.back == 1:
            self.back = 0
            self.name = '陌客'
            self.type = 'outsider'
            self.good = 1
            self.firstPriority = 29
            self.priority = 39

