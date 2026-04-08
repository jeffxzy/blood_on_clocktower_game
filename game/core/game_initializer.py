import random
import copy
from typing import List, Dict, Any, Optional

from nonebot.log import logger

from ..models.player_config import PlayerConfig
from ..config.game_config import GameConfig
from ..identities.IdentityClass import Identity
from ..identities.ImportIdentities import importAll, importExpect


class GameInitializer:
    """
    游戏初始化器
    
    负责处理游戏的初始化逻辑，包括：
    - 配置板子
    - 分配角色
    - 初始化玩家
    """
    
    def __init__(self, game: Any):
        self.game = game
    
    def initialize(self) -> bool:
        """
        执行游戏初始化
        
        Returns:
            是否初始化成功
        """
        if not self._setup_game_board():
            return False
        
        if self.game.status == 'stop':
            return False
        
        self._add_nobody_identity()
        self._assign_roles()
        self._check_and_adjust_blacksmith()
        self._validate_outsider_count()
        self._assign_townsfolk_and_outsiders()
        self._readd_blacksmith_if_needed()
        self._shuffle_seats()
        self._initialize_players()
        
        return True
    
    def _setup_game_board(self) -> bool:
        """设置游戏板子"""
        if self.game.config == 0:
            return self._setup_custom_board()
        
        setup = GameConfig.get_setup(self.game.config)
        if setup is None:
            logger.warning(f"板子配置 {self.game.config} 不存在，使用默认板子 1")
            self.game.config = 1
            setup = GameConfig.get_default_setup()
        else:
            logger.info(f"使用板子配置: {self.game.config} ({setup.name})")
        
        self.game.cName = setup.name
        self.game.playerNum = setup.player_config.to_list()
        self.game.identityAll = importAll(self.game.cName)
        
        return True
    
    def _setup_custom_board(self) -> bool:
        """设置自定义板子"""
        self.game.cName = '自定义'
        self.game.identityAll = importExpect(self.game.expectIdentities)
        
        if len(self.game.playerNum) != 5:
            self.game.retBoard = '[错误] 没有定义板子'
            self.game.status = 'stop'
            return False
        
        if self.game.playerNum[0] <= 2:
            self.game.retBoard = '[错误] 游戏人数不足'
            self.game.status = 'stop'
            return False
        
        if len(self.game.identityAll['outsider']) < self.game.playerNum[2]:
            self.game.retBoard = '[错误] 外来者数量小于预期'
            self.game.status = 'stop'
            return False
        
        if len(self.game.identityAll['minion']) < self.game.playerNum[3]:
            self.game.retBoard = '[错误] 爪牙数量小于预期'
            self.game.status = 'stop'
            return False
        
        if len(self.game.identityAll['demon']) < self.game.playerNum[4]:
            self.game.retBoard = '[错误] 恶魔数量小于预期'
            self.game.status = 'stop'
            return False
        
        if len(self.game.identityAll['townsfolk']) < self.game.playerNum[0]:
            self.game.retBoard = '[错误] 镇民数量小于预期，镇民数量必须至少为所有玩家数量。'
            self.game.status = 'stop'
            return False
        
        return True
    
    def _add_nobody_identity(self) -> None:
        """添加空身份（用于座位0）"""
        self.game.players.append(self.game.identityAll['nobody'][0])
    
    def _assign_roles(self) -> None:
        """分配爪牙和恶魔角色"""
        # 分配爪牙
        for i in range(self.game.playerNum[3]):
            self._add_role('minion', i)
        
        # 分配恶魔
        for i in range(self.game.playerNum[4]):
            self._add_role('demon', i)
    
    def _add_role(self, role_type: str, index: int) -> None:
        """添加单个角色并处理外来者调整"""
        identity = copy.deepcopy(self.game.identityAll[role_type][index])
        self.game.players.append(identity)
        self.game.identityAll[role_type][index].used = 1
        
        if identity.changeOutsiders != 0:
            self.game.playerNum[1] -= identity.changeOutsiders
            self.game.playerNum[2] += identity.changeOutsiders
    
    def _check_and_adjust_blacksmith(self) -> None:
        """检查铁匠并调整外来者数量"""
        self.game.hasBlacksmith = 0
        self.game.blacksmith_index = -1
        
        for i in range(len(self.game.identityAll['townsfolk'])):
            if (self.game.identityAll['townsfolk'][i].name == '铁匠' 
                    and i < self.game.playerNum[1]):
                self.game.hasBlacksmith = 1
                self.game.blacksmith_index = i
                break
        
        if self.game.hasBlacksmith == 1:
            blacksmith = self.game.identityAll['townsfolk'][self.game.blacksmith_index]
            if blacksmith.changeOutsiders != 0:
                self.game.playerNum[1] -= blacksmith.changeOutsiders
                self.game.playerNum[2] += blacksmith.changeOutsiders
            self.game.allBoard += '铁匠在场，+1外来者。\n\n'
    
    def _validate_outsider_count(self) -> None:
        """验证并调整外来者数量"""
        if self.game.playerNum[2] < 0:
            self.game.playerNum[1] += self.game.playerNum[2]
            self.game.playerNum[2] = 0
            self.game.allBoard += '外来者数量小于0，已经强制置为0。\n\n'
        elif self.game.playerNum[2] > len(self.game.identityAll['outsider']):
            excess = self.game.playerNum[2] - len(self.game.identityAll['outsider'])
            self.game.playerNum[1] += excess
            self.game.playerNum[2] = len(self.game.identityAll['outsider'])
            self.game.allBoard += f'外来者数量超过板子中外来者总数，已经强制置为{len(self.game.identityAll["outsider"])}。\n\n'
    
    def _assign_townsfolk_and_outsiders(self) -> None:
        """分配镇民和外来者"""
        for i in range(self.game.playerNum[1]):
            self._add_role_from_pool('townsfolk', i)
        
        for i in range(self.game.playerNum[2]):
            self._add_role_from_pool('outsider', i)
    
    def _add_role_from_pool(self, role_type: str, index: int) -> None:
        """从角色池中添加角色"""
        identity = copy.deepcopy(self.game.identityAll[role_type][index])
        self.game.players.append(identity)
        self.game.identityAll[role_type][index].used = 1
    
    def _readd_blacksmith_if_needed(self) -> None:
        """如果需要，重新添加铁匠"""
        if self.game.hasBlacksmith == 1:
            for i in range(len(self.game.identityAll['townsfolk'])):
                if (self.game.identityAll['townsfolk'][i].name == '铁匠' 
                        and self.game.identityAll['townsfolk'][i].used == 0):
                    blacksmith = copy.deepcopy(self.game.identityAll['townsfolk'][i])
                    self.game.players.append(blacksmith)
                    self.game.identityAll['townsfolk'][i].used = 1
                    break
    
    def _shuffle_seats(self) -> None:
        """打乱座位顺序，确保空身份在第一位"""
        shuffle_count = 0
        while shuffle_count < 1000:
            shuffle_count += 1
            random.shuffle(self.game.players)
            if self.game.players[0].name == '空':
                break
    
    def _initialize_players(self) -> None:
        """初始化所有玩家"""
        self.game.dayBoard.append('')
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].seat = i
            self.game.dayBoard.append('')
        
        # 特殊初始化
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].specInit(self.game)
        
        # 坏人伪装身份
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].redPretend(self.game)
        
        # 自我介绍
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].introduce(self.game)
        
        # 记录玩家信息
        self._record_players()
    
    def _record_players(self) -> None:
        """记录所有玩家信息到allBoard"""
        for i in range(1, self.game.playerNum[0] + 1):
            player = self.game.players[i]
            if player.type in ['townsfolk', 'outsider']:
                self.game.allBoard += '🔵'
            elif player.type in ['minion', 'demon']:
                self.game.allBoard += '🔴'
            self.game.allBoard += f' {i}号：{player.name}\n'
