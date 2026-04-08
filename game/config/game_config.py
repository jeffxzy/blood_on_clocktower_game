from dataclasses import dataclass
from typing import Dict, List, Optional

from ..models.player_config import PlayerConfig


@dataclass
class GameSetup:
    """单个游戏板子配置"""
    name: str
    player_config: PlayerConfig
    townsfolk_names: List[str]
    outsider_names: List[str]
    minion_names: List[str]
    demon_names: List[str]


class GameConfig:
    """游戏配置管理类"""
    
    # 板子配置映射
    _SETUPS: Dict[int, GameSetup] = {}
    
    @classmethod
    def initialize(cls) -> None:
        """初始化所有板子配置"""
        cls._SETUPS = {
            1: GameSetup(
                name='标准1',
                player_config=PlayerConfig(12, 7, 2, 2, 1),
                townsfolk_names=[
                    '调查员', '厨师', '钟表匠', '占卜师', '算命师', '贵族', '缝匠',
                    '洗衣妇', '哲学家', '做梦者', '送葬者', '艺术家', '共情者', '铁匠', '祖母'
                ],
                outsider_names=['心上人', '酒鬼', '隐士', '修补匠'],
                minion_names=['教父', '刺客', '寡妇', '间谍'],
                demon_names=['诺达西', ' FangGu', '小鬼', '利维坦']
            ),
            2: GameSetup(
                name='利维坦1',
                player_config=PlayerConfig(6, 3, 1, 1, 1),
                townsfolk_names=['调查员', '钟表匠', '哲学家', '做梦者', '送葬者', '算命师'],
                outsider_names=['酒鬼', '心上人'],
                minion_names=['寡妇', '教父'],
                demon_names=['利维坦']
            ),
            3: GameSetup(
                name='华灯1',
                player_config=PlayerConfig(8, 5, 1, 1, 1),
                townsfolk_names=[
                    '占星师', '舞狮者', '调查员', '钟表匠', '做梦者', '缝匠',
                    '占卜师', '哲学家', '共情者', '算命师', '祖母'
                ],
                outsider_names=['酒鬼', '心上人', '调酒师'],
                minion_names=['寡妇', '教父', '刺客'],
                demon_names=['典狱长', '饕餮', 'FangGu']
            ),
            4: GameSetup(
                name='华灯2',
                player_config=PlayerConfig(12, 7, 2, 2, 1),
                townsfolk_names=[
                    '占星师', '舞狮者', '厨师', '钟表匠', '做梦者', '缝匠',
                    '占卜师', '哲学家', '共情者', '算命师', '艺术家', '贵族',
                    '图书管理员', '祖母'
                ],
                outsider_names=['酒鬼', '心上人', '调酒师', '修补匠'],
                minion_names=['寡妇', '教父', '刺客', '邪恶双子'],
                demon_names=['典狱长', '饕餮', '诺达西', 'Po']
            ),
            5: GameSetup(
                name='投毒1',
                player_config=PlayerConfig(8, 5, 1, 1, 1),
                townsfolk_names=[
                    '占星师', '钟表匠', '做梦者', '缝匠', '占卜师', '哲学家',
                    '算命师', '调查员', '图书管理员', '贵族', '共情者', '祖母'
                ],
                outsider_names=['酒鬼'],
                minion_names=['投毒者'],
                demon_names=['小鬼']
            )
        }
    
    @classmethod
    def get_setup(cls, config_id: int) -> Optional[GameSetup]:
        """
        获取指定配置的板子设置
        
        Args:
            config_id: 配置ID
            
        Returns:
            GameSetup 对象，如果不存在返回 None
        """
        if not cls._SETUPS:
            cls.initialize()
        return cls._SETUPS.get(config_id)
    
    @classmethod
    def get_default_setup(cls) -> GameSetup:
        """获取默认配置（标准1）"""
        setup = cls.get_setup(1)
        if setup is None:
            raise RuntimeError("默认配置不存在")
        return setup
    
    @classmethod
    def get_max_config(cls) -> int:
        """获取最大配置ID"""
        if not cls._SETUPS:
            cls.initialize()
        return max(cls._SETUPS.keys()) if cls._SETUPS else 0
