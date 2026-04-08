import random
from .MinionClass import *

class Spy(Minion):
    def init(self):
        self.name = '间谍'
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
                if self.hasPretend:
                    r = random.randint(1, 10)
                    if r <= 7:
                        self.back = 1
                        self.name = self.pretend.name
                        self.type = self.pretend.type
                        self.good = 1
                        self.firstPriority = 79
                        self.priority = 79
                        game.allBoard += str(self.seat) + '号间谍今晚接下来被视作' + self.name + '\n'
                        return
        if self.back == 1:
            self.back = 0
            self.name = '间谍'
            self.type = 'minion'
            self.good = 0
            self.firstPriority = 29
            self.priority = 39

