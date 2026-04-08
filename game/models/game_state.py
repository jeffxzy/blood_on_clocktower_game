from enum import Enum, auto


class GameStatus(Enum):
    """游戏状态枚举，替代原来的字符串状态"""
    STOPPED = auto()
    INITIALIZING = auto()
    STARTED = auto()
    NIGHT = auto()
    DAY = auto()
    
    @classmethod
    def from_string(cls, status_str: str) -> 'GameStatus':
        """从字符串转换为枚举，保持向后兼容"""
        mapping = {
            'stop': cls.STOPPED,
            'init': cls.INITIALIZING,
            'started': cls.STARTED,
            'night': cls.NIGHT,
            'day': cls.DAY
        }
        return mapping.get(status_str, cls.STOPPED)
    
    def to_string(self) -> str:
        """转换为字符串，保持向后兼容"""
        mapping = {
            GameStatus.STOPPED: 'stop',
            GameStatus.INITIALIZING: 'init',
            GameStatus.STARTED: 'started',
            GameStatus.NIGHT: 'night',
            GameStatus.DAY: 'day'
        }
        return mapping.get(self, 'stop')
