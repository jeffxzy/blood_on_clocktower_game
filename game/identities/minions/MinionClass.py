import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.IdentityClass import *

class Minion(Identity):
    def identityInit(self):
        self.type = 'minion'

    