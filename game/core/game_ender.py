from typing import Any


class GameEnder:
    """
    游戏结束检查器
    
    负责检查游戏是否应该结束
    """
    
    def __init__(self, game: Any):
        self.game = game
    
    def check_game_end(self) -> bool:
        """
        检查游戏是否结束
        
        Returns:
            游戏是否已结束
        """
        # 先处理下午状态
        for i in range(1, self.game.playerNum[0] + 1):
            self.game.players[i].afternoon(self.game)
        
        # 检查恶魔是否全部死亡
        if self._check_all_demons_dead():
            self._end_with_good_victory()
            return True
        
        # 检查存活玩家是否过少
        if self._check_too_few_players():
            self._end_with_evil_victory()
            return True
        
        return False
    
    def _check_all_demons_dead(self) -> bool:
        """检查是否所有恶魔都死亡"""
        has_alive_demon = False
        for i in range(1, self.game.playerNum[0] + 1):
            player = self.game.players[i]
            if player.type == 'demon' and player.alive == 1:
                has_alive_demon = True
                break
        return not has_alive_demon
    
    def _check_too_few_players(self) -> bool:
        """检查存活玩家是否过少（<=2人）"""
        alive_count = 0
        for i in range(1, self.game.playerNum[0] + 1):
            if self.game.players[i].alive == 1:
                alive_count += 1
        return alive_count <= 2
    
    def _end_with_good_victory(self) -> None:
        """善良阵营获胜"""
        self.game.status = 'stop'
        self.game.allBoard += '\n\n善良获胜。'
    
    def _end_with_evil_victory(self) -> None:
        """邪恶阵营获胜"""
        self.game.status = 'stop'
        self.game.allBoard += '\n\n邪恶获胜。'
