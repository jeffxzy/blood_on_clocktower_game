import random
from .TownsfolkClass import *

class Gambler(Townsfolk):

    def init(self):
        self.name = '赌徒'
        self.priority = 20

    def night(self, game):
        if self.alive == 1:
            # 随机选择一名玩家并猜测角色
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    break
            
            if r1 != 0:
                # 随机猜测一个角色
                guess_name = game.players[r1].name
                
                if self.healthy == 0:
                    # 中毒时随机决定是否猜对，即使猜错也不会死亡
                    if random.randint(1, 2) == 1:
                        game.dayBoard[self.seat] += '猜测' + str(r1) + '号是' + guess_name + '，猜对了'
                        game.allBoard += str(self.seat) + '号赌徒猜测' + str(r1) + '号是' + guess_name + '，猜对了\n'
                    else:
                        game.dayBoard[self.seat] += '猜测' + str(r1) + '号是' + guess_name + '，猜错了，但由于中毒不会死亡'
                        game.allBoard += str(self.seat) + '号赌徒猜测' + str(r1) + '号是' + guess_name + '，猜错了，但由于中毒不会死亡\n'
                else:
                    # 健康状态下
                    if game.players[r1].name == guess_name:
                        game.dayBoard[self.seat] += '猜测' + str(r1) + '号是' + guess_name + '，猜对了'
                        game.allBoard += str(self.seat) + '号赌徒猜测' + str(r1) + '号是' + guess_name + '，猜对了\n'
                    else:
                        game.dayBoard[self.seat] += '猜测' + str(r1) + '号是' + guess_name + '，猜错了，死亡'
                        game.allBoard += str(self.seat) + '号赌徒猜测' + str(r1) + '号是' + guess_name + '，猜错了，死亡\n'
                        self.killed(game)
        return
