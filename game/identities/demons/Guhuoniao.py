import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.demons.DemonClass import *

class Guhuoniao(Demon):

    def init(self):
        self.name = '姑获鸟'
        self.priority = 77
        self.hasAbsorbed = 0
        self.absorbedAbility = None
        self.back = 0
        self.originalName = '姑获鸟'
        self.originalType = 'demon'
        self.originalGood = 0
        self.originalPriority = 77

    def night(self, game):
        # 选择一名玩家死亡
        if self.alive == 1:
            # 首先执行姑获鸟的基本能力：杀死一名玩家
            cnt = 0
            r1 = 0
            while cnt < 1000:
                cnt = cnt + 1
                r1 = random.randint(1, game.playerNum[0])
                if r1 != self.seat and game.players[r1].alive == 1:
                    break
            
            if r1 != 0:
                game.allBoard += str(self.seat) + '号姑获鸟杀死了' + str(r1) + '号\n'
                game.players[r1].killed(game)
            
            # 如果吸收了刺客的能力，使用刺客的刺杀能力
            if self.hasAbsorbed == 1 and self.absorbedAbility == '刺客':
                # 选择一名玩家刺杀
                cnt = 0
                r2 = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r2 = random.randint(1, game.playerNum[0])
                    if r2 != self.seat and game.players[r2].alive == 1:
                        break
                
                if r2 != 0:
                    game.allBoard += str(self.seat) + '号姑获鸟使用刺客能力刺杀了' + str(r2) + '号\n'
                    if game.players[r2].type == 'demon':
                        # 如果刺杀的是恶魔，姑获鸟死亡
                        game.allBoard += str(self.seat) + '号姑获鸟刺杀了恶魔，自己死亡\n'
                        self.killed(game)
                    else:
                        # 否则，被刺杀的玩家死亡
                        game.players[r2].killed(game)
            
            # 如果吸收了教父的能力，使用教父的能力
            elif self.hasAbsorbed == 1 and self.absorbedAbility == '教父':
                # 选择一名非恶魔玩家
                cnt = 0
                r3 = 0
                while cnt < 1000:
                    cnt = cnt + 1
                    r3 = random.randint(1, game.playerNum[0])
                    if r3 != self.seat and game.players[r3].alive == 1 and game.players[r3].type != 'demon':
                        break
                
                if r3 != 0 and game.lastDied != 0 and game.players[game.lastDied].type == 'outsider':
                    game.allBoard += str(self.seat) + '号姑获鸟使用教父能力杀死了' + str(r3) + '号\n'
                    game.players[r3].killed(game)
            
            # 如果吸收了间谍的能力，使用间谍的能力
            elif self.hasAbsorbed == 1 and self.absorbedAbility == '间谍':
                # 间谍能力：在当晚被查验时被认为是好人
                if self.back == 0 and self.healthy != 0:
                    # 模拟间谍能力，将自己伪装成好人
                    self.back = 1
                    self.name = '村民'
                    self.type = 'townsfolk'
                    self.good = 1
                    self.priority = 99
                    game.allBoard += str(self.seat) + '号姑获鸟使用间谍能力，今晚被视作好人\n'
            
            # 如果吸收了红唇女郎的能力，什么能力都没有
            elif self.hasAbsorbed == 1 and self.absorbedAbility == '红唇女郎':
                # 红唇女郎没有特殊能力，姑获鸟吸收后也不会获得任何能力
                pass
        return

    def dayAction(self, game):
        # 恢复原始状态（如果使用了间谍能力）
        if self.back == 1:
            self.back = 0
            self.name = self.originalName
            self.type = self.originalType
            self.good = self.originalGood
            self.priority = self.originalPriority
        
        # 检查是否有爪牙死于处决，只吸取第一名被处决的爪牙的能力
        if self.alive == 1 and self.hasAbsorbed == 0:
            # 遍历所有玩家，找到第一个死亡的爪牙
            for i in range(1, game.playerNum[0] + 1):
                if game.players[i].type == 'minion' and game.players[i].alive == 0:
                    # 吸收爪牙的能力
                    self.hasAbsorbed = 1
                    self.absorbedAbility = game.players[i].name
                    game.allBoard += str(self.seat) + '号姑获鸟吸收了' + str(i) + '号爪牙的能力\n'
                    break
        return
