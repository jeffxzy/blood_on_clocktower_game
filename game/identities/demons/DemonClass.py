import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.IdentityClass import *

class Demon(Identity):
    def identityInit(self):
        self.type = 'demon'

    def checkGrandmotherDeath(self, game, killedSeat):
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].name == '祖母' and hasattr(game.players[i], 'checkGrandchildDeath'):
                game.players[i].checkGrandchildDeath(game, killedSeat, True)

    