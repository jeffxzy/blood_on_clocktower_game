import random
from .TownsfolkClass import *

class Nobody(Townsfolk):

    # 这个角色只是占位的。不应该看到这个角色。
    def init(self):
        self.name = '空'
