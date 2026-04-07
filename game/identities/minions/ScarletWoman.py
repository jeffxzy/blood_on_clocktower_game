import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.minions.MinionClass import *

class ScarletWoman(Minion):

    def init(self):
        self.name = '红唇女郎'
        self.priority = 37
        self.becameDemon = 0

    def night(self, game):
        # 检查恶魔是否死亡，如果死亡且存活玩家>=5，变成恶魔
        if self.alive == 1 and self.becameDemon == 0:
            demon_alive = 0
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'demon' and game.players[i].alive == 1:
                    demon_alive = 1
                    break
            
            if demon_alive == 0:
                # 计算存活玩家数
                lives = 0
                for i in range(1, game.playerNum[0] + 1):
                    if game.players[i].alive == 1:
                        lives = lives + 1
                
                if lives >= 5:
                    self.becameDemon = 1
                    self.type = 'demon'
                    game.allBoard += str(self.seat) + '号红唇女郎变成了恶魔\n'
        return
