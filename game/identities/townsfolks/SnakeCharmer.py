import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class SnakeCharmer(Townsfolk):

    def init(self):
        self.name = '舞蛇人'
        self.priority = 21

    def night(self, game):
        if self.alive == 1:
            # 选择一名存活的玩家
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    break
            
            if r1 != 0:
                # 检查选中的玩家是否是恶魔
                if game.players[r1].type == 'demon':
                    # 交换角色和阵营
                    game.allBoard += str(self.seat) + '号舞蛇人选中了恶魔，交换角色和阵营\n'
                    
                    # 保存原舞蛇人和原恶魔的信息
                    original_snake_charmer_seat = self.seat
                    original_demon_seat = r1
                    
                    # 保存原恶魔的类型
                    original_demon_name = game.players[r1].name
                    
                    # 交换角色
                    temp_name = self.name
                    temp_type = self.type
                    temp_good = self.good
                    temp_priority = self.priority
                    
                    self.name = game.players[r1].name
                    self.type = game.players[r1].type
                    self.good = game.players[r1].good
                    self.priority = game.players[r1].priority
                    
                    game.players[r1].name = temp_name
                    game.players[r1].type = temp_type
                    game.players[r1].good = temp_good
                    game.players[r1].priority = temp_priority
                    
                    # 原恶魔（现在的舞蛇人）中毒并说出自己原本的恶魔类型
                    game.players[r1].healthy = 0
                    game.allBoard += str(r1) + '号现在是舞蛇人，并且中毒了\n'
                    game.allBoard += str(r1) + '号说：“我原本是' + original_demon_name + '！”\n'
                else:
                    # 没有选中恶魔，什么都不发生
                    pass
        return