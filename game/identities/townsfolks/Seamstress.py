import random
from .TownsfolkClass import *

class Seamstress(Townsfolk):

    def init(self):
        self.name = '女裁缝'
        self.firstPriority = 42

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            # 避免死循环
            fin = '是'

            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat:
                    break
            while cnt < 1000:
                cnt = cnt + 1
                r2 = random.randint(1, game.playerNum[0])
                if r2 != self.seat and r2 != r1:
                    break
            if game.players[r1].good == game.players[r2].good:
                fin = '是'
            else:
                fin = '否'
            if self.healthy == 0:
                if fin == '是':
                    fin = '否'
                else:
                    fin = '是'

            if r1 > r2:
                r1, r2 = r2, r1

            game.dayBoard[self.seat] += str(r1) + '/' + str(r2) + fin
            game.allBoard += str(self.seat) + '号女裁缝选择了' + str(r1) + '/' + str(r2) + fin + '\n'

        return
