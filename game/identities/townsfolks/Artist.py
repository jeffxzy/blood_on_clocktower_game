import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Artist(Townsfolk):

    def init(self):
        self.name = '艺术家'
        self.firstPriority = 80

    def firstNight(self, game):
        # 查看是否还活着
        if self.alive == 1:
            que = '无问题'
            fin = '我不知道'
            if random.randint(1,2) == 1:
                que = '奇数位置有恶魔吗？'
                fin = '否'
                for i in range(1, game.playerNum[0]):
                    if i % 2 == 1 and game.players[i].type == 'demon':
                        fin = '是'
            elif random.randint(1,1) == 1:
                que = '邪恶玩家序号和是奇数吗？'
                sum = 0
                for i in range(1, game.playerNum[0]):
                    if game.players[i].good == 0:
                        sum = sum + i
                if sum % 2 == 1:
                    fin = '是'
                else:
                    fin = '否'

            if self.healthy == 0:
                if fin == '是':
                    fin = '否'
                else:
                    fin = '是'

            game.dayBoard[self.seat] += '我询问' + que + '得知' + fin + ' '
            game.allBoard += str(self.seat) + '号艺术家询问' + que + '得知' + fin + '\n'

        return
