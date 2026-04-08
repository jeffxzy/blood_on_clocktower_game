import random
from enum import Enum

import copy

class Status(Enum):
    IS_EVIL = 'isEvil'
    IS_DRUNK = 'IsDrunk'
    LEARN_FAILED = 'LearnFailed'
    PHILOSOPHER = 'philosopher'
    BLACKSMITH = 'blacksmith'
    SWEETHEART = 'sweetheart'
    BARTENDER = 'bartender'
    WIDOW = 'widow'
    POISONER = 'poisoner'
    NO_DASHII = 'NoDashii'
    IS_NEW_FANGGU = 'isNewFangGu'

class Identity():


    def __init__(self):
        # 名字
        self.name = ''
        # 类别
        self.type = ''
        # 存活
        self.alive = 1
        # 序号
        self.seat = 0
        # 坏状态
        self.drunk = []
        self.poisoned = []
        self.vortex = []
        # 行动顺次
        self.firstPriority = 0
        self.priority = 0
        # 健康状态
        self.healthy = 1
        # 是否为好人
        self.good = 1
        # 是否有额外身份
        self.hasPretend = 0
        # 额外身份
        self.pretend = ''
        # 这个身份是否已经存在场上
        self.used = 0

        # 子类1的初始化
        self.identityInit()
        # 子类2的初始化
        self.init()
        return
    
    # 标准初始化
    def init(self, game):
        pass
    # 特殊初始化
    def specInit(self, game):
        pass
    # 红进行身份伪装
    def redPretend(self, game):
        if self.type == 'demon' or self.type == 'minion':
            self.good = 0
            # 小概率伪装成外来者
            for i in range(0, len(game.identityAll['outsider'])):
                if game.identityAll['outsider'][i].used == 0 and game.identityAll['outsider'][i].name != '酒鬼':
                    if random.randint(1, 8) == 1:
                        self.hasPretend = 1
                        self.pretend = copy.deepcopy(game.identityAll['outsider'][i])
                        self.pretend.seat = self.seat
                        game.identityAll['outsider'][i].used = 1
                        self.pretend.poisoned.append(Status.IS_EVIL)
                    # logger.info('我是' + str(self.seat) + '，我刚刚虚构了一个身份：' + self.pretend.name + '\n')
                        return
                    # 失败了也不再重试
                    break
            for i in range(0, len(game.identityAll['townsfolk'])):
                if game.identityAll['townsfolk'][i].used == 0:
                    self.hasPretend = 1
                    self.pretend = copy.deepcopy(game.identityAll['townsfolk'][i])
                    self.pretend.seat = self.seat
                    game.identityAll['townsfolk'][i].used = 1
                    self.pretend.poisoned.append('isEvil')
                    # logger.info('我是' + str(self.seat) + '，我刚刚虚构了一个身份：' + self.pretend.name + '\n')
                    return
        
    
    # 检查自己的坏状态
    def check(self):
        if self.drunk == [] and self.poisoned == [] and self.vortex == []:
            self.healthy = 1
        else:
            self.healthy = 0
        return

    # 清除过时的怀状态
    def afternoon(self, game):
        if Status.POISONER in self.poisoned:
            self.poisoned.remove(Status.POISONER)
        if self.hasPretend == 1 and Status.POISONER in self.pretend.poisoned:
            self.pretend.poisoned.remove(Status.POISONER)

    # 第一天的自我介绍
    def introduce(self, game):
        game.dayBoard[self.seat] = str(self.seat) + '号:'
        if self.hasPretend == 0 or self.name == '哲学家':
            game.dayBoard[self.seat] += self.name
            if self.type == 'outsider':
                game.dayBoard[self.seat] += ' (外来者)'
        else:
            game.dayBoard[self.seat] += self.pretend.name
            if self.pretend.type == 'outsider':
                game.dayBoard[self.seat] += ' (外来者)'
        game.dayBoard[self.seat] += '  '
        return

    # 首个夜晚开始前的检查
    def preFirstNight(self, game):
        self.check()
        return
    # 首个夜晚操作
    def firstNight(self, game):
        return
    # 每个夜晚*开始前的检查
    def preNight(self, game):
        self.check()
        return
    # 每个夜晚*操作
    def night(self, game):
        return
    # 死亡时
    def killed(self, game):
        if self.alive == 0:
            return
        self.alive = 0
        if self.hasPretend == 1:
            self.pretend.killed(game)
        else:
            pass
        return
