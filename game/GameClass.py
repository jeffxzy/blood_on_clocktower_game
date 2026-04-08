import random
import os
from typing import List, Dict, Any, Optional

from nonebot.log import logger

from ._read import *
from .Alarm import *
from .Rand import *

from .identities.IdentityClass import *
from .identities.ImportIdentities import *
from .core.game_initializer import GameInitializer
from .core.day_manager import DayManager
from .core.game_ender import GameEnder
from .config.game_config import GameConfig

import copy


class Game:
    """
    游戏主类
    
    负责协调各个组件完成游戏流程，保持向后兼容性
    """

    def __init__(self):
        # 群聊id
        self.group_id: str = '0'
        # 游戏状态
        self.status: str = 'stop'
        # 当天信息记录
        self.dayBoard: List[str] = []
        # 当天信息综合
        self.retBoard: str = ''
        # 对局状态记录
        self.allBoard: str = ''
        # 参与玩家
        self.users: List[Any] = []
        # 所有被加入的身份
        self.identityAll: Dict[str, List[Any]] = []
        # 游戏内的玩家
        self.players: List[Any] = []
        # 游戏玩家数（保持向后兼容，新代码建议使用 PlayerConfig）
        self.playerNum: List[int] = []
        # 游戏当前天数
        self.days: int = 0
        # 白天死亡玩家
        self.lastDied: int = 0
        # 游戏设置
        self.config: int = 1
        # 板子总数
        self.maxConfig: int = 5
        # 自定义角色
        self.expectIdentities: List[int] = []
        # 当前板子名称
        self.cName: str = ''
        
        # 铁匠相关临时变量
        self.hasBlacksmith: int = 0
        self.blacksmith_index: int = -1
        
        # 初始化组件
        self._initializer: Optional[GameInitializer] = None
        self._day_manager: Optional[DayManager] = None
        self._game_ender: Optional[GameEnder] = None
        
        # 初始化配置
        GameConfig.initialize()
        self.maxConfig = GameConfig.get_max_config()

    def test(self) -> str:
        """测试方法"""
        print("开始测试")
        self.init()
        print("初始化完成")
        for i in range(1, self.playerNum[0] + 1):
            print(str(i) + "号：" + self.players[i].name)
        self.day()
        print("一天执行完成")
        return self.retBoard

    def init(self) -> None:
        """
        游戏初始化
        
        使用 GameInitializer 组件完成初始化逻辑
        """
        self._initializer = GameInitializer(self)
        self._initializer.initialize()

    def day(self) -> None:
        """
        运行一天
        
        使用 DayManager 组件完成天数逻辑
        """
        if self._day_manager is None:
            self._day_manager = DayManager(self)
        self._day_manager.run_day()

    def gameEndCheck(self) -> bool:
        """
        检查游戏是否结束
        
        使用 GameEnder 组件完成结束检查
        """
        if self._game_ender is None:
            self._game_ender = GameEnder(self)
        return self._game_ender.check_game_end()

    def getRandomIdentity(self, game: Any, type_str: str) -> Any:
        """
        获取随机身份
        
        Args:
            game: 游戏对象
            type_str: 身份类型字符串，'1'=镇民, '2'=外来者, '3'=爪牙, '4'=恶魔
            
        Returns:
            随机选择的身份
        """
        candidates: List[Any] = []
        if '1' in type_str and len(self.identityAll['townsfolk']) != 0:
            candidates.append(self.identityAll['townsfolk'][random.randint(0, len(self.identityAll['townsfolk']) - 1)])
        if '2' in type_str and len(self.identityAll['outsider']) != 0:
            candidates.append(self.identityAll['outsider'][random.randint(0, len(self.identityAll['outsider']) - 1)])
        if '3' in type_str and len(self.identityAll['minion']) != 0:
            candidates.append(self.identityAll['minion'][random.randint(0, len(self.identityAll['minion']) - 1)])
        if '4' in type_str and len(self.identityAll['demon']) != 0:
            candidates.append(self.identityAll['demon'][random.randint(0, len(self.identityAll['demon']) - 1)])
        return candidates[random.randint(0, len(candidates) - 1)]
