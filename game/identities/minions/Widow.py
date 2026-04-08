import random
from .MinionClass import *

class Widow(Minion):

    def init(self):
        self.name = '寡妇'
        self.firstPriority = 18
    
    def firstNight(self, game):
        # 检查存活
        if self.alive == 1:
            # 检查坏状态
            if self.healthy == 0:
                return
            # 避免死循环
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if game.players[r1].type == 'townsfolk':
                    break

            # 自毒
            if random.randint(0, 1) == 0:
                game.players[self.seat].poisoned.append('widow')
                game.allBoard += str(self.seat) + '号寡妇毒了自己' + '\n'

                # 自报寡妇
                if random.randint(0, 1) == 0:
                    game.dayBoard[self.seat] += '我得知寡妇。'
            else:
                if game.players[r1].hasPretend == 1:
                    game.players[r1].pretend.poisoned.append('widow')
                else:
                    game.players[r1].poisoned.append('widow')
                game.allBoard += str(self.seat) + '号寡妇毒了' + str(r1) + '\n'

                while cnt < 1000:
                    cnt = cnt + 1
                    r2 = random.randint(1, game.playerNum[0])
                    if game.players[r2].good == 1:
                        break

                game.dayBoard[r2] += '我得知寡妇。'
                game.allBoard += str(r2) + '得知寡妇在场\n'
                return

    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        if self.hasPretend == 1:
            self.pretend.killed(game)
        for i in range(1, game.playerNum[0] + 1):
            if 'widow' in game.players[i].poisoned:
                game.players[i].poisoned.remove('widow')
                game.allBoard += str(i) + '号因寡妇的中毒消除了\n'

