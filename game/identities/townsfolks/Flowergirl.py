import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Flowergirl(Townsfolk):

    def init(self):
        self.name = '卖花女孩'
        self.priority = 116

    def night(self, game):
        if self.alive == 1:
            # 模拟昨天的投票情况
            voted_players = []
            demon_voted = False
            
            # 随机决定哪些玩家投票了（70%的概率投票）
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].alive == 1 and random.random() < 0.7:
                    voted_players.append(i)
                    # 检查是否是恶魔
                    if game.players[i].type == 'demon':
                        demon_voted = True
            
            if self.healthy == 0:
                # 中毒时可能得到错误信息
                demon_voted = not demon_voted
            
            # 生成投票玩家列表字符串
            voted_str = ''
            if voted_players:
                voted_str = '、'.join(map(str, voted_players)) + '号'
            else:
                voted_str = '没有人'
            
            # 生成信息
            if demon_voted:
                message = f'昨天{ voted_str }投票了，其中恶魔投票了'
            else:
                message = f'昨天{ voted_str }投票了，恶魔没有投票'
            
            game.dayBoard[self.seat] += message
            game.allBoard += str(self.seat) + '号卖花女孩得知：' + message + '\n'
        return
