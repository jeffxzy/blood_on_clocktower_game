import random
import os

from nonebot.log import logger
from src.plugins._read import *

from src.plugins.game.identities.townsfolks.TownsfolkClass import *

class Nobody(Townsfolk):

    # 这个角色只是占位的。不应该看到这个角色。
    def init(self):
        self.name = '空'
