import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.outsiders.OutsiderClass import *

class Puzzlemaster(Outsider):

    def init(self):
        self.name = '解谜大师'
        self.poisonedTarget = 0
        self.hasGuessed = 0

    def specInit(self, game):
        # 随机选择一名玩家让他醉酒
        cnt = 0
        while cnt < 1000:
            cnt = cnt + 1
            r1 = random.randint(1, game.playerNum[0])
            if r1 != self.seat:
                self.poisonedTarget = r1
                game.players[r1].healthy = 0
                break
        return

    def dayAction(self, game):
        # 白天可以猜测谁是醉酒玩家
        if self.alive == 1 and self.hasGuessed == 0:
            # 随机猜测一名玩家
            cnt = 0
            guess = 0
            while cnt < 1000:
                cnt = cnt + 1
                guess = random.randint(1, game.playerNum[0])
                if guess != self.seat:
                    break
            
            self.hasGuessed = 1
            
            # 检查是否有存活的铁匠
            has_alive_blacksmith = False
            is_guess_blacksmith = False
            is_poisoned_blacksmith = False
            
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].alive == 1 and game.players[i].name == '铁匠':
                    has_alive_blacksmith = True
                if i == guess and game.players[i].name == '铁匠':
                    is_guess_blacksmith = True
                if i == self.poisonedTarget and game.players[i].name == '铁匠':
                    is_poisoned_blacksmith = True
            
            # 检查是否猜对了
            if guess == self.poisonedTarget:
                # 检查是否符合特殊条件：中毒的不是铁匠，且有存活的铁匠在场，且猜测的是铁匠
                if not is_poisoned_blacksmith and has_alive_blacksmith and is_guess_blacksmith:
                    # 即使猜对了，也得知错误的恶魔信息
                    wrong_demon = random.randint(1, game.playerNum[0])
                    while wrong_demon == self.seat or game.players[wrong_demon].type == 'demon':
                        wrong_demon = random.randint(1, game.playerNum[0])
                    game.dayBoard[self.seat] += '猜测' + str(guess) + '号醉酒，猜错了。错误信息：恶魔是' + str(wrong_demon) + '号'
                    game.allBoard += str(self.seat) + '号解谜大师猜测' + str(guess) + '号醉酒，猜错了。错误信息：恶魔是' + str(wrong_demon) + '号\n'
                else:
                    # 猜对了，得知恶魔是谁
                    demon_seat = 0
                    for i in range(1, game.playerNum[0] + 1):
                        if game.players[i].type == 'demon':
                            demon_seat = i
                            break
                    game.dayBoard[self.seat] += '猜测' + str(guess) + '号醉酒，猜对了！恶魔是' + str(demon_seat) + '号'
                    game.allBoard += str(self.seat) + '号解谜大师猜测' + str(guess) + '号醉酒，猜对了！得知恶魔是' + str(demon_seat) + '号\n'
            else:
                # 猜错了，得知错误的恶魔信息
                wrong_demon = random.randint(1, game.playerNum[0])
                while wrong_demon == self.seat or game.players[wrong_demon].type == 'demon':
                    wrong_demon = random.randint(1, game.playerNum[0])
                game.dayBoard[self.seat] += '猜测' + str(guess) + '号醉酒，猜错了。错误信息：恶魔是' + str(wrong_demon) + '号'
                game.allBoard += str(self.seat) + '号解谜大师猜测' + str(guess) + '号醉酒，猜错了。错误信息：恶魔是' + str(wrong_demon) + '号\n'
        return
