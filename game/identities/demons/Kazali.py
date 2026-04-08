import random
import os

from nonebot.log import logger
from .DemonClass import *

class Kazali(Demon):

    def init(self):
        self.name = '卡扎力'
        self.firstPriority = 10
        self.priority = 77

    def firstNight(self, game):
        # 卡扎力的特殊能力：选择玩家变成邪恶爪牙，并指定爪牙角色
        if self.alive == 1:
            # 计算需要选择的爪牙数量
            player_count = game.playerNum[0]
            minion_count = 1 if player_count <= 9 else 2
            
            # 可选的爪牙角色
            minion_roles = ['刺客', '间谍', '红唇女郎', '教父']
            
            # 选择玩家变成爪牙
            selected = []
            for _ in range(minion_count):
                cnt = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r1 = random.randint(1, game.playerNum[0])
                    if r1 != self.seat and game.players[r1].type != 'demon' and r1 not in selected:
                        # 选择一个爪牙角色
                        if minion_roles:
                            minion_role = random.choice(minion_roles)
                            # 移除已选择的角色，避免重复
                            minion_roles.remove(minion_role)
                        else:
                            # 如果没有可选角色，使用默认角色
                            minion_role = '刺客'
                        
                        # 标记为邪恶爪牙
                        game.players[r1].good = 0
                        game.players[r1].type = 'minion'
                        game.players[r1].name = minion_role
                        
                        game.allBoard += str(self.seat) + '号卡扎力让' + str(r1) + '号变成了邪恶爪牙' + minion_role + '\n'
                        selected.append(r1)
                        break
        return

    def night(self, game):
        # 选择一名玩家死亡
        if self.alive == 1:
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    break
            
            if r1 != 0:
                game.allBoard += str(self.seat) + '号卡扎力杀死了' + str(r1) + '号\n'
                game.players[r1].killed(game)
        return
