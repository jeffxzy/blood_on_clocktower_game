import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.outsiders.OutsiderClass import *

class Barber(Outsider):

    def init(self):
        self.name = '理发师'
        self.priority = 96
        self.diedToday = 0

    def killed(self, game):
        if self.alive == 1:
            self.alive = 0
            self.diedToday = 1
            game.allBoard += str(self.seat) + '号理发师死亡\n'
        return

    def night(self, game):
        # 如果理发师今天死亡且未中毒，恶魔可以交换两名玩家的角色
        if self.diedToday == 1 and self.healthy != 0:
            self.diedToday = 0
            # 找到恶魔
            demon_seat = 0
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'demon' and game.players[i].alive == 1:
                    demon_seat = i
                    break
            
            if demon_seat != 0:
                # 恶魔选择两名玩家交换角色（简化实现）
                cnt = 0
                r1, r2 = 0, 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r1 = random.randint(1, game.playerNum[0])
                    if r1 != demon_seat and game.players[r1].type != 'demon':
                        r2 = r1
                        while (r2 == r1 or r2 == demon_seat or game.players[r2].type == 'demon') and cnt < 1000:
                            cnt = cnt + 1
                            r2 = random.randint(1, game.playerNum[0])
                        break
                
                if r1 != 0 and r2 != 0:
                    # 交换角色
                    game.allBoard += str(demon_seat) + '号恶魔通过理发师能力交换了' + str(r1) + '号和' + str(r2) + '号的角色\n'
        return
