import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.IdentityClass import *

class Townsfolk(Identity):

    def identityInit(self):
        self.type = 'townsfolk'
