import random
from .TownsfolkClass import *

class Undertaker(Townsfolk):

    def init(self):
        self.name = '送葬者'
        self.priority = 56

    def night(self, game):
        # 查看是否还活着
        if self.alive == 1:
            if game.lastDied == 0:
                return
            fin = game.players[game.lastDied].name

            if self.healthy == 0:
                # 邪恶的伪装：3/4概率给正确信息
                if 'isEvil' in self.poisoned and random.randint(1, 4) <= 3:
                    pass
                else:
                    cnt = 0
                    while cnt < 1000:
                        cnt = cnt + 1
                        r = game.getRandomIdentity(game, '123')
                        if r.name != fin:
                            if random.randint(1, 10) <= 5:
                                fin = r.name
                            break

            game.dayBoard[self.seat] += '挖' + str(game.lastDied) + fin + ' '
            game.allBoard += str(self.seat) + '号送葬者挖' + str(game.lastDied) + fin + '\n'

        return
