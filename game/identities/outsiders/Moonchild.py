import random
from .OutsiderClass import *

class Moonchild(Outsider):

    def init(self):
        self.name = '月之子'
        self.priority = 93
        self.target = 0
        self.dead = 0

    def killed(self, game):
        if self.alive == 1:
            self.alive = 0
            self.dead = 1
            # 月之子死亡，选择一名存活玩家
            cnt = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    self.target = r1
                    break
            
            if self.target != 0:
                game.allBoard += str(self.seat) + '号月之子死亡，选择了' + str(self.target) + '号\n'
        return

    def night(self, game):
        # 如果月之子死亡并选择了目标，且月之子在死亡时是健康的
        if self.dead == 1 and self.target != 0:
            # 检查月之子在死亡时是否健康（未中毒）
            if self.healthy != 0 and game.players[self.target].good == 1:
                # 目标是善良的，目标死亡
                game.allBoard += str(self.target) + '号被月之子能力杀死\n'
                game.players[self.target].killed(game)
            self.target = 0
        return
