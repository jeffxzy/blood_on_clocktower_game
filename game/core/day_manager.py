from typing import Any


class DayManager:
    """
    天数管理器
    
    负责处理游戏中的天数逻辑，包括：
    - 夜晚行动
    - 白天转换
    - 状态管理
    """
    
    def __init__(self, game: Any):
        self.game = game
    
    def run_day(self) -> None:
        """运行一天的游戏流程"""
        if self.game.status == 'stop':
            return
        
        self.game.status = 'night'
        
        # 处理下午状态
        self._process_afternoon()
        
        # 检查游戏是否结束
        if self.game.gameEndCheck():
            return
        
        # 增加天数
        self._increment_day()
        
        # 执行夜晚行动
        self._execute_night_actions()
        
        # 准备返回信息
        self._prepare_return_board()
        
        self.game.status = 'day'
        
        # 再次检查游戏是否结束
        if self.game.gameEndCheck():
            return
    
    def _process_afternoon(self) -> None:
        """处理下午状态（清除过期状态）"""
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].afternoon(self.game)
    
    def _increment_day(self) -> None:
        """增加天数并更新记录"""
        self.game.days += 1
        self.game.dayBoard[0] = f'【第 {self.game.days} 天】\n'
        self.game.allBoard += f'\n【第 {self.game.days} 天】\n'
    
    def _execute_night_actions(self) -> None:
        """执行夜晚行动"""
        for priority in range(1, 100):
            if self.game.days == 1:
                self._execute_first_night_actions(priority)
            else:
                self._execute_regular_night_actions(priority)
    
    def _execute_first_night_actions(self, priority: int) -> None:
        """执行首夜行动"""
        for i in range(1, self.game.playerNum[0] + 1):
            current = self.game.players[i]
            loop_count = 0
            
            while loop_count < 1000:
                if current.firstPriority == priority:
                    current.preFirstNight(self.game)
                    current.firstNight(self.game)
                
                if current.hasPretend != 1:
                    break
                else:
                    current = current.pretend
                loop_count += 1
    
    def _execute_regular_night_actions(self, priority: int) -> None:
        """执行普通夜晚行动"""
        for i in range(1, self.game.playerNum[0] + 1):
            current = self.game.players[i]
            loop_count = 0
            
            while loop_count < 1000:
                if current.priority == priority:
                    current.preNight(self.game)
                    current.night(self.game)
                
                if current.hasPretend != 1:
                    break
                else:
                    current = current.pretend
                loop_count += 1
    
    def _prepare_return_board(self) -> None:
        """准备返回信息板"""
        self.game.retBoard = ''
        for i in range(self.game.playerNum[0] + 1):
            if i != 0 and self.game.players[i].alive == 0:
                self.game.retBoard += '❌'
            self.game.retBoard += self.game.dayBoard[i] + '\n'
