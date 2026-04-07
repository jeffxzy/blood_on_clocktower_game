import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Investigator(Townsfolk):

    def init(self):
        self.name = '调查员'
        self.firstPriority = 34

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            # 避免死循环
            cnt = 0
            r1, r2, see = 0, 0, ''
            while cnt < 1000:
                cnt = cnt + 1
                # 选取随机玩家
                r1 = random.randint(1, game.playerNum[0])
                if game.players[r1].type == 'minion':
                    see = game.players[r1].name
                    r2 = r1
                    while (r2 == r1 or r2 == self.seat) and cnt < 1000:
                        r2 = random.randint(1, game.playerNum[0])
                    # 坏状态检查
                    if self.healthy == 0:
                        r3 = r1
                        while (r3 == r1 or r3 == r2 or r3 == self.seat) and cnt < 1000:
                            cnt = cnt + 1
                            r3 = random.randint(1, game.playerNum[0])
                        r1 = r3
                        if random.randint(1, 3) == 1:
                            r = random.randint(0, len(game.identityAll['minion']) - 1)
                            see = game.identityAll['minion'][r].name
                    break
            
            if r1 > r2:
                r1, r2 = r2, r1
            
            if r1 == 0 or r2 == 0:
                game.dayBoard[self.seat] += '我得知没有任何爪牙在场。'
                game.allBoard += str(self.seat) + '号调查员得知没有爪牙在场。\n'
            else:
                game.dayBoard[self.seat] += str(r1) + '/' + str(r2) + see
                game.allBoard += str(self.seat) + '号调查员得知' + str(r1) + '/' + str(r2) + see + '\n'
        return