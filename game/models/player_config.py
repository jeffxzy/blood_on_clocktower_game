from dataclasses import dataclass
from typing import List


@dataclass
class PlayerConfig:
    """
    玩家数量配置类，封装各种角色的数量
    
    替代原来的 playerNum 数组，提高代码可读性
    """
    total_players: int
    townsfolk_count: int
    outsider_count: int
    minion_count: int
    demon_count: int
    
    @classmethod
    def from_list(cls, numbers: List[int]) -> 'PlayerConfig':
        """从列表创建配置，保持向后兼容"""
        if len(numbers) != 5:
            raise ValueError("PlayerConfig 需要 5 个数字：[总人数, 镇民, 外来者, 爪牙, 恶魔]")
        return cls(
            total_players=numbers[0],
            townsfolk_count=numbers[1],
            outsider_count=numbers[2],
            minion_count=numbers[3],
            demon_count=numbers[4]
        )
    
    def to_list(self) -> List[int]:
        """转换为列表，保持向后兼容"""
        return [
            self.total_players,
            self.townsfolk_count,
            self.outsider_count,
            self.minion_count,
            self.demon_count
        ]
    
    def adjust_outsiders(self, delta: int) -> None:
        """
        调整外来者数量，并相应调整镇民数量
        
        Args:
            delta: 外来者数量的变化值（正数表示增加外来者，减少镇民）
        """
        self.townsfolk_count -= delta
        self.outsider_count += delta
