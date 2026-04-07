import random
import os

from nonebot.log import logger

from src.plugins._read import *
from src.plugins.Alarm import *
from src.plugins.Rand import *
# from src.plugins.characters.CharacterClass import *

from src.plugins.game.identities.IdentityClass import *
from src.plugins.game.identities.ImportIdentities import *

import copy

class Game:
    


    def __init__(self):
        # 群聊id
        self.group_id = '0'
        # 游戏状态
        self.status = 'stop'
        # 当天信息记录
        self.dayBoard = []
        # 当天信息综合
        self.retBoard = ''
        # 对局状态记录
        self.allBoard = ''
        # 参与玩家
        self.users = []
        # 所有被加入的身份
        self.identityAll = []
        # 游戏内的玩家
        self.players = []
        # 游戏玩家数
        self.playerNum = []
        # 游戏当前天数
        self.days = 0
        # 白天死亡玩家
        self.lastDied = 0
        # 游戏设置
        self.config = 1
        # 板子总数
        self.maxConfig = 5
        # 自定义角色
        self.expectIdentities = []

        return

    def test(self):
        print("开始测试")
        self.init()
        print("初始化完成")
        for i in range(1, self.playerNum[0] + 1):
            print(str(i) + "号：" + self.players[i].name)
        self.day()
        print("一天执行完成")

        return self.retBoard

    def init(self):

        # 确定板子
        self.cName = ''
        if self.config == 1:
            self.cName = '标准1'
            self.playerNum = [8, 5, 1, 1, 1]
        elif self.config == 2:
            self.cName = '利维坦1'
            self.playerNum = [6, 3, 1, 1, 1]
        elif self.config == 3:
            self.cName = '华灯1'
            self.playerNum = [8, 5, 1, 1, 1]
        elif self.config == 4:
            self.cName = '华灯2'
            self.playerNum = [12, 7, 2, 2, 1]
        elif self.config == 5:
            self.cName = '投毒1'
            self.playerNum = [8, 5, 1, 1, 1]
        elif self.config != 0:
            self.config = 1
            self.cName = '标准1'
            self.playerNum = [12, 7, 2, 2, 1]
        # 根据板子名初始化
        if self.cName != '':
            self.identityAll = importAll(self.cName)

        # 特判自定义板子
        if self.config == 0:
            self.cName = '自定义'
            self.identityAll = importExpect(self.expectIdentities)
            if len(self.playerNum) != 5:
                self.retBoard = '[错误] 没有定义板子'
                self.status = 'stop'
                return
            if self.playerNum[0] <= 2:
                self.retBoard = '[错误] 游戏人数不足'
                self.status = 'stop'
            # if len(self.identityAll['townsfolk']) < self.playerNum[1]:
            #     self.retBoard = '[错误] 镇民数量小于预期'
            #     self.status = 'stop'
            if len(self.identityAll['outsider']) < self.playerNum[2]:
                self.retBoard = '[错误] 外来者数量小于预期'
                self.status = 'stop'
            if len(self.identityAll['minion']) < self.playerNum[3]:
                self.retBoard = '[错误] 爪牙数量小于预期'
                self.status = 'stop'
            if len(self.identityAll['demon']) < self.playerNum[4]:
                self.retBoard = '[错误] 恶魔数量小于预期'
                self.status = 'stop'
            if len(self.identityAll['townsfolk']) < self.playerNum[0]:
                self.retBoard = '[错误] 镇民数量小于预期，镇民数量必须至少为所有玩家数量。'
                self.status = 'stop'

        if self.status == 'stop':
            return


        self.players.append(self.identityAll['nobody'][0])

        # 按爪牙 恶魔 镇民 外来的顺序读入角色
        for i in range(0, self.playerNum[3]):
            self.players.append(copy.deepcopy(self.identityAll['minion'][i]))
            self.identityAll['minion'][i].used = 1
            # 教父有1/5概率-1外来者
            if self.identityAll['minion'][i].name == '教父':
                p = 1
                if random.randint(1, 5) == 5:
                    p = -1
                self.playerNum[1] = self.playerNum[1] - p
                self.playerNum[2] = self.playerNum[2] + p

        for i in range(0, self.playerNum[4]):
            self.players.append(copy.deepcopy(self.identityAll['demon'][i]))
            self.identityAll['demon'][i].used = 1
            if self.identityAll['demon'][i].name == '方古':
                self.playerNum[1] = self.playerNum[1] - 1
                self.playerNum[2] = self.playerNum[2] + 1
            if self.identityAll['demon'][i].name == '梼杌':
                self.playerNum[1] = self.playerNum[1] - 1
                self.playerNum[2] = self.playerNum[2] + 1

        # 检查是否有铁匠
        hasBlacksmith = 0
        for i in range(0, len(self.identityAll['townsfolk'])):
            if self.identityAll['townsfolk'][i].name == '铁匠' and i < self.playerNum[1]:
                hasBlacksmith = 1
                break
        if hasBlacksmith == 1:
            self.playerNum[1] = self.playerNum[1] - 1
            self.playerNum[2] = self.playerNum[2] + 1
            self.allBoard += '铁匠在场，+1外来者。\n\n'

        # 外来数量不能小于0或大于板子中外来者总数
        if self.playerNum[2] < 0:
            self.playerNum[1] = self.playerNum[1] + self.playerNum[2]
            self.playerNum[2] = 0
            self.allBoard += '外来者数量小于0，已经强制置为0。\n\n'
        elif self.playerNum[2] > len(self.identityAll['outsider']):
            excess = self.playerNum[2] - len(self.identityAll['outsider'])
            self.playerNum[1] = self.playerNum[1] + excess
            self.playerNum[2] = len(self.identityAll['outsider'])
            self.allBoard += '外来者数量超过板子中外来者总数，已经强制置为' + str(len(self.identityAll['outsider'])) + '。\n\n'

        for i in range(0, self.playerNum[1]):
            self.players.append(copy.deepcopy(self.identityAll['townsfolk'][i]))
            self.identityAll['townsfolk'][i].used = 1

        for i in range(0, self.playerNum[2]):
            self.players.append(copy.deepcopy(self.identityAll['outsider'][i]))
            self.identityAll['outsider'][i].used = 1

        # 重新添加铁匠（如果存在）
        if hasBlacksmith == 1:
            for i in range(0, len(self.identityAll['townsfolk'])):
                if self.identityAll['townsfolk'][i].name == '铁匠' and self.identityAll['townsfolk'][i].used == 0:
                    self.players.append(copy.deepcopy(self.identityAll['townsfolk'][i]))
                    self.identityAll['townsfolk'][i].used = 1
                    break

        # 打乱座位
        cnt = 0
        while cnt < 1000:
            cnt = cnt + 1
            random.shuffle(self.players)
            if self.players[0].name == '空':
                break
        # 初始化
        self.dayBoard.append('')
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].seat = i
            self.players[i].init()
            self.dayBoard.append('')
        # 所有人特殊初始化
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].specInit(self)
        # 让坏人寻找一个合适的身份
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].redPretend(self)
        # 所有人自我介绍
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].introduce(self)

        for i in range(1, self.playerNum[0] + 1):
            if self.players[i].type == 'townsfolk':
                self.allBoard += '🔵'
            if self.players[i].type == 'outsider':
                self.allBoard += '🔵'
            if self.players[i].type == 'minion':
                self.allBoard += '🔴'
            if self.players[i].type == 'demon':
                self.allBoard += '🔴'
            self.allBoard += ' ' + str(i) + "号：" + self.players[i].name + '\n'


    def day(self):

        # 游戏是否因为意外原因结束
        if self.status == 'stop':
            return

        self.status = 'night'

        # 处理消失的坏状态
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].afternoon(self)

        # 检查游戏是否结束
        if self.gameEndCheck() == True:
            return


        # 加一天
        self.days = self.days + 1
        self.dayBoard[0] = '【第 ' + str(self.days) + ' 天】\n'
        self.allBoard += '\n【第 ' + str(self.days) + ' 天】\n'

        for pri in range(1, 100):
            if self.days == 1:
                for i in range(1, self.playerNum[0] + 1):
                    # 首夜可行动
                    now = self.players[i]
                    cnt = 0
                    while cnt < 1000:
                        if now.firstPriority == pri:
                            now.preFirstNight(self)
                            now.firstNight(self)
                        if now.hasPretend != 1:
                            break
                        else:
                            now = now.pretend
            else:
                for i in range(1, self.playerNum[0] + 1):
                    # 每个夜晚*可行动
                    now = self.players[i]
                    cnt = 0
                    while cnt < 1000:
                        if now.priority == pri:
                            now.preNight(self)
                            now.night(self)
                        if now.hasPretend != 1:
                            break
                        else:
                            now = now.pretend
        self.retBoard = ''
        for i in range(0, self.playerNum[0] + 1):
            if i != 0 and self.players[i].alive == 0:
                self.retBoard +='❌'
            self.retBoard += self.dayBoard[i] + '\n'

        self.status = 'day'

        # 检查游戏是否结束
        if self.gameEndCheck() == True:
            return

        return

    def gameEndCheck(self):
        # 检查游戏是否结束（恶魔死亡）
        cont = 0
        for i in range(1, self.playerNum[0] + 1):
            self.players[i].afternoon(self)
            if self.players[i].type == 'demon' and self.players[i].alive == 1:
                cont = 1
        if cont == 0:
            self.status = 'stop'
            self.allBoard += '\n\n善良获胜。'
            return True
        # 检查游戏是否结束（玩家不足）
        lives = 0
        for i in range(1, self.playerNum[0] + 1):
            if self.players[i].alive == 1:
                lives = lives + 1
        if lives <= 2:
            self.status = 'stop'
            self.allBoard += '\n\n邪恶获胜。'
            return True
        return False

    def getRandomIdentity(self, game, str):
        r = []
        if '1' in str and len(self.identityAll['townsfolk']) != 0:
            r.append(self.identityAll['townsfolk'][random.randint(0, len(self.identityAll['townsfolk']) - 1)])
        if '2' in str and len(self.identityAll['outsider']) != 0:
            r.append(self.identityAll['outsider'][random.randint(0, len(self.identityAll['outsider']) - 1)])
        if '3' in str and len(self.identityAll['minion']) != 0:
            r.append(self.identityAll['minion'][random.randint(0, len(self.identityAll['minion']) - 1)])
        if '4' in str and len(self.identityAll['demon']) != 0:
            r.append(self.identityAll['demon'][random.randint(0, len(self.identityAll['demon']) - 1)])
        return r[random.randint(0, len(r) - 1)]