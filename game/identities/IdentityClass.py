import random
from enum import Enum
from typing import List, Any, Optional

import copy


class Status(Enum):
    """身份状态枚举"""
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


class Identity:
    """
    身份基类
    
    所有游戏角色的基础类，定义了角色的通用属性和方法
    """

    def __init__(self):
        # 名字
        self.name: str = ''
        # 类别
        self.type: str = ''
        # 存活状态（1=存活，0=死亡）
        self.alive: int = 1
        # 座位号
        self.seat: int = 0
        # 坏状态列表
        self.drunk: List[Status] = []
        self.poisoned: List[Any] = []
        self.vortex: List[Any] = []
        # 行动顺序（首夜和普通夜）
        self.firstPriority: int = 0
        self.priority: int = 0
        # 健康状态（1=健康，0=不健康）
        self.healthy: int = 1
        # 是否为好人阵营（1=好人，0=坏人）
        self.good: int = 1
        # 是否有伪装身份
        self.hasPretend: int = 0
        # 伪装身份对象
        self.pretend: Optional['Identity'] = None
        # 该身份是否已被使用
        self.used: int = 0
        # 改变外来者数量的属性
        self.changeOutsiders: int = 0

        # 子类1的初始化（设置身份类型）
        self.identityInit()
        # 子类2的初始化（设置身份具体属性）
        self.init()

    def init(self, game: Any = None) -> None:
        """
        标准初始化
        
        子类可以覆盖此方法进行额外的初始化
        """
        pass

    def specInit(self, game: Any) -> None:
        """
        特殊初始化
        
        在游戏开始时调用，用于执行需要游戏上下文的初始化
        """
        pass

    def redPretend(self, game: Any) -> None:
        """
        坏人身份伪装
        
        让恶魔和爪牙伪装成好人身份
        """
        if self.type == 'demon' or self.type == 'minion':
            self.good = 0
            
            # 小概率伪装成外来者（非酒鬼）
            for i in range(len(game.identityAll['outsider'])):
                outsider = game.identityAll['outsider'][i]
                if outsider.used == 0 and outsider.name != '酒鬼':
                    if random.randint(1, 8) == 1:
                        self._set_pretend_identity(outsider, game)
                        return
                    break
            
            # 伪装成镇民
            for i in range(len(game.identityAll['townsfolk'])):
                townsfolk = game.identityAll['townsfolk'][i]
                if townsfolk.used == 0:
                    self._set_pretend_identity(townsfolk, game)
                    return

    def _set_pretend_identity(self, identity: 'Identity', game: Any) -> None:
        """
        设置伪装身份
        
        Args:
            identity: 要伪装成的身份
            game: 游戏对象
        """
        self.hasPretend = 1
        self.pretend = copy.deepcopy(identity)
        self.pretend.seat = self.seat
        identity.used = 1
        self.pretend.poisoned.append(Status.IS_EVIL)

    def check(self) -> None:
        """
        检查健康状态
        
        根据当前状态更新 healthy 属性
        """
        if not self.drunk and not self.poisoned and not self.vortex:
            self.healthy = 1
        else:
            self.healthy = 0

    def afternoon(self, game: Any) -> None:
        """
        下午处理
        
        清除过期的状态（如投毒者的毒）
        """
        if Status.POISONER in self.poisoned:
            self.poisoned.remove(Status.POISONER)
        if self.hasPretend == 1 and self.pretend and Status.POISONER in self.pretend.poisoned:
            self.pretend.poisoned.remove(Status.POISONER)

    def introduce(self, game: Any) -> None:
        """
        自我介绍
        
        在首夜向所有人介绍自己的身份
        """
        game.dayBoard[self.seat] = f'{self.seat}号:'
        
        # 哲学家或者没有伪装的情况显示真实身份
        if self.hasPretend == 0 or self.name == '哲学家':
            game.dayBoard[self.seat] += self.name
            if self.type == 'outsider':
                game.dayBoard[self.seat] += ' (外来者)'
        else:
            # 有伪装的情况显示伪装身份
            if self.pretend:
                game.dayBoard[self.seat] += self.pretend.name
                if self.pretend.type == 'outsider':
                    game.dayBoard[self.seat] += ' (外来者)'
        
        game.dayBoard[self.seat] += '  '

    def preFirstNight(self, game: Any) -> None:
        """
        首夜开始前的准备
        
        在首夜行动前调用
        """
        self.check()

    def firstNight(self, game: Any) -> None:
        """
        首夜行动
        
        子类可以覆盖此方法实现首夜特殊能力
        """
        pass

    def preNight(self, game: Any) -> None:
        """
        普通夜晚开始前的准备
        
        在每个夜晚行动前调用
        """
        self.check()

    def night(self, game: Any) -> None:
        """
        普通夜晚行动
        
        子类可以覆盖此方法实现夜晚特殊能力
        """
        pass

    def killed(self, game: Any) -> None:
        """
        死亡处理
        
        当角色死亡时调用
        """
        if self.alive == 0:
            return
        
        self.alive = 0
        if self.hasPretend == 1 and self.pretend:
            self.pretend.killed(game)

