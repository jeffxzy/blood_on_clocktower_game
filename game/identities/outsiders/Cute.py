import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.outsiders.OutsiderClass import *

class Cute(Outsider):
    def init(self):
        self.name = '白板外来者'