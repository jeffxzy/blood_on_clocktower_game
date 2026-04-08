import random
from typing import Optional, Callable, Tuple

from .TownsfolkClass import *


class Grandmother(Townsfolk):
    MAX_RANDOM_ATTEMPTS = 1000
    EVIL_SHOW_PROBABILITY = 80
    DRUNK_SHOW_PROBABILITY = 90
    SPY_SURVIVAL_PROBABILITY = 70

    def init(self):
        self.name = '祖母'
        self.firstPriority = 35
        self.grandchildSeat = 0
        self.firstNightHealthy = 1

    def specInit(self, game):
        self.firstNightHealthy = 1

    def _get_player_display_name(self, player) -> str:
        if player.name == '酒鬼':
            return '酒鬼'
        elif player.name == '哲学家':
            return '哲学家'
        elif player.hasPretend == 1:
            return player.pretend.name
        else:
            return player.name

    def _find_random_player(self, game, validate_func: Callable[[int], bool]) -> int:
        for _ in range(self.MAX_RANDOM_ATTEMPTS):
            seat = random.randint(1, game.playerNum[0])
            if validate_func(seat):
                return seat
        return 0

    def _is_misinformation_active(self) -> bool:
        return self.firstNightHealthy == 0 or Status.IS_EVIL in self.poisoned

    def _get_real_grandchild(self, game) -> int:
        return self._find_random_player(
            game,
            lambda seat: seat != self.seat and game.players[seat].good == 1
        )

    def _get_evil_player(self, game) -> int:
        return self._find_random_player(
            game,
            lambda seat: seat != self.seat and game.players[seat].good == 0
        )

    def _get_any_other_player(self, game) -> int:
        return self._find_random_player(
            game,
            lambda seat: seat != self.seat
        )

    def _determine_misinformation(self, game, real_grandchild: int) -> Tuple[int, str]:
        roll = random.randint(1, 100)
        if roll <= self.EVIL_SHOW_PROBABILITY:
            show_seat = self._get_evil_player(game)
            show_name = self._get_player_display_name(game.players[show_seat])
        elif roll <= self.DRUNK_SHOW_PROBABILITY:
            show_seat = self._get_any_other_player(game)
            show_name = '酒鬼'
        else:
            show_seat = self._get_any_other_player(game)
            show_name = self._get_player_display_name(game.players[show_seat])
        return show_seat, show_name

    def _record_grandchild_info(self, game, show_seat: int, show_name: str):
        game.dayBoard[self.seat] += f'{show_seat}号玩家是你的孙子，他是{show_name}'
        game.allBoard += f'{self.seat}号祖母得知{show_seat}号是他的孙子，他是{show_name}\n'

    def firstNight(self, game):
        if self.alive == 0:
            return

        self.check()
        if self.healthy == 0:
            self.firstNightHealthy = 0

        real_grandchild = self._get_real_grandchild(game)
        self.grandchildSeat = real_grandchild

        show_seat = real_grandchild
        show_name = self._get_player_display_name(game.players[real_grandchild])

        if self._is_misinformation_active():
            show_seat, show_name = self._determine_misinformation(game, real_grandchild)

        self._record_grandchild_info(game, show_seat, show_name)

    def _should_die_with_grandchild(self, game, killed_seat: int, killed_by_demon: bool) -> bool:
        if self.alive == 0:
            return False
        if killed_seat != self.grandchildSeat:
            return False
        if not killed_by_demon:
            return False
        
        self.check()
        if self.healthy == 0 or self.firstNightHealthy == 0:
            return False
        
        return True

    def _is_grandchild_spy(self, game, killed_seat: int) -> bool:
        return hasattr(game.players[killed_seat], 'back')

    def _handle_spy_grandchild_death(self, game, killed_seat: int):
        roll = random.randint(1, 100)
        if roll <= self.SPY_SURVIVAL_PROBABILITY:
            game.allBoard += f'{self.seat}号祖母因孙子{killed_seat}号（间谍）被恶魔杀死而一同死亡\n'
            self.killed(game)
        else:
            game.allBoard += f'{self.seat}号祖母的孙子{killed_seat}号（间谍）被恶魔杀死，但祖母侥幸存活\n'

    def _handle_normal_grandchild_death(self, game, killed_seat: int):
        game.allBoard += f'{self.seat}号祖母因孙子{killed_seat}号被恶魔杀死而一同死亡\n'
        self.killed(game)

    def checkGrandchildDeath(self, game, killed_seat: int, killed_by_demon: bool):
        if not self._should_die_with_grandchild(game, killed_seat, killed_by_demon):
            return

        if self._is_grandchild_spy(game, killed_seat):
            self._handle_spy_grandchild_death(game, killed_seat)
        else:
            self._handle_normal_grandchild_death(game, killed_seat)
