import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class FangGu(Demon):
    def init(self):
        self.name = '方古'
        self.priority = 29
        self.used = 0
        self.newSeat = 0

    def night(self, game):
        # 检查是否有理发师健康死亡
        barber_swap = hasattr(game, 'barber_died_healthy') and game.barber_died_healthy
        
        if barber_swap:
            # 理发师健康死亡，恶魔可以选择两名玩家交换角色
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1 and game.players[r1].type != 'demon':
                    break
            
            cnt = 0
            r2 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r2 = random.randint(1, game.playerNum[0])
                if r2 != self.seat and r2 != r1 and game.players[r2].alive == 1 and game.players[r2].type != 'demon':
                    break
            
            if r1 != 0 and r2 != 0:
                # 交换两名玩家的角色
                temp_name = game.players[r1].name
                temp_type = game.players[r1].type
                temp_good = game.players[r1].good
                
                game.players[r1].name = game.players[r2].name
                game.players[r1].type = game.players[r2].type
                game.players[r1].good = game.players[r2].good
                
                game.players[r2].name = temp_name
                game.players[r2].type = temp_type
                game.players[r2].good = temp_good
                
                game.allBoard += str(self.seat) + '号方古利用理发师的能力，交换了' + str(r1) + '号和' + str(r2) + '号的角色。\n'
                return  # 交换后直接返回，不执行杀人逻辑
        
        # 正常杀人逻辑
        cnt = 0
        r1 = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat and game.players[r1].alive == 1 and game.players[r1].type != 'demon':
                break
        
        if r1 == 0:
            return
        
        # 检查是否满足杀人条件
        can_kill = False
        if self.alive == 1 and self.healthy != 0:
            can_kill = True
        elif self.newSeat > 0 and self.newSeat <= game.playerNum[0]:
            if game.players[self.newSeat].alive == 1:
                # 检查新方古的poisoned列表
                if hasattr(game.players[self.newSeat], 'poisoned'):
                    if len(game.players[self.newSeat].poisoned) <= 1:
                        can_kill = True
                else:
                    # 如果poisoned属性不存在，可以杀人
                    can_kill = True
        
        if not can_kill:
            game.allBoard += str(self.seat) + '号方古今晚无法杀人。\n'
            return
        
        # 传刀逻辑
        if game.players[r1].type == 'outsider' and self.used == 0:
            self.used = 1
            self.killed(game)
            self.newSeat = r1
            game.players[r1].name = '方古'
            game.players[r1].type = 'demon'
            game.players[r1].good = 0
            # 确保poisoned列表存在
            if not hasattr(game.players[r1], 'poisoned'):
                game.players[r1].poisoned = []
            game.players[r1].poisoned.append('isNewFangGu')
            game.allBoard += str(self.seat) + '号方古杀死了自己\n' + str(r1) + '号变成了邪恶的方古\n'
            return
        
        # 正常杀人
        if self.used == 0:
            game.allBoard += str(self.seat) + '号方古杀死了' + str(r1) + '号\n'
        else:
            game.allBoard += str(self.seat) + '号方古借' + str(self.newSeat) + '号之力杀死了' + str(r1) + '号\n'
        game.players[r1].killed(game)
        self.checkGrandmotherDeath(game, r1)
