import random
import os
from datetime import date
from datetime import datetime
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot.log import logger

from src.plugins._read import *
from src.plugins.Alarm import *

from src.plugins.game.GameClass import *
from src.plugins.game.UserClass import *


async def ProcessGame(bot: Bot, event: Event, game, group_id, user_id, text, message):

    sl = ['init']
    kl = ['开始', 'start']
    await RunFunc(StartGame, sl, kl, bot, event, game, group_id, user_id, text, message)

    sl = ['started', 'day', 'night']
    kl = ['处决', 'kill', '空过', 'pass']
    await RunFunc(DayGame, sl, kl, bot, event, game, group_id, user_id, text, message)

    sl = ['init', 'started', 'day', 'night']
    kl = ['板子', 'pic']
    await RunFunc(GetPic, sl, kl, bot, event, game, group_id, user_id, text, message)

    sl = ['init']
    kl = ['人物', '角色', '添加', '设置']
    await RunFunc(AddConfig, sl, kl, bot, event, game, group_id, user_id, text, message)

    return


async def RunFunc(func, statusList, keywordList, bot: Bot, event: Event, game, group_id, user_id, text, message):

    ok = 0
    for i in keywordList:
        if i in text:
            ok = 1

    if ok == 0:
        return

    ok = 0
    for i in statusList:
        if i == game.status:
            ok = 1

    if ok == 0:
        message = '[错误] 这个指令只有在以下状态可用：\n'
        for i in range(0, len(statusList)):
            if i != 0:
                message += ' / '
            message += statusList[i]
        message += '\n而游戏现在的状态是：\n' + game.status
        await bot.send_group_msg(group_id=group_id, message=message)
        return

    await func(bot, event, game, group_id, user_id, text, message)
    return


async def StartGame(bot: Bot, event: Event, game, group_id, user_id, text, message):

    game.status = 'started'
    game.init()
    game.day()
    
    message = '游戏开始。\n当前板子：' + game.cName + '\n您可发送 。pic 查看当前板子图片。'
    await bot.send_group_msg(group_id=group_id, message=message)
    
    message = game.retBoard

    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def DayGame(bot: Bot, event: Event, game, group_id, user_id, text, message):

    id = getNumber(text, 0)
    if id < 0 or id > game.playerNum[0]:
        message = '[错误] ' + str(id) + ' 不是一个有效的处决目标。'
        await bot.send_group_msg(group_id=group_id, message=message)
        return
    if id != 0:
        if game.players[id].alive == 1:
            game.lastDied = id
        else:
            game.lastDied = 0
        game.allBoard += str(id) + '号被处决\n'
        game.players[id].killed(game)
        
        hasLeviathan = False
        grandmotherSeat = 0
        isGrandchild = False
        grandmotherHealthy = False
        
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].name == '利维坦' and game.players[i].alive == 1:
                hasLeviathan = True
            if game.players[i].name == '祖母' and hasattr(game.players[i], 'grandchildSeat'):
                grandmotherSeat = i
                if game.players[i].grandchildSeat == id:
                    isGrandchild = True
                game.players[i].check()
                if game.players[i].healthy == 1 and hasattr(game.players[i], 'firstNightHealthy') and game.players[i].firstNightHealthy == 1:
                    grandmotherHealthy = True
        
        if hasLeviathan and isGrandchild and grandmotherHealthy:
            game.allBoard += '利维坦在场，且祖母的孙子被处决，邪恶阵营获胜！\n'
            for i in range(1, game.playerNum[0] + 1):
                if i != grandmotherSeat and game.players[i].name != '利维坦':
                    game.players[i].killed(game)
            game.status = 'stop'
    else:
        game.lastDied = 0
        game.allBoard += '平安日，无人被处决\n'
    game.day()
    if game.status == 'stop':
        message = '游戏结束。'
        await bot.send_group_msg(group_id=group_id, message=message)
        message = game.allBoard
        await bot.send_group_msg(group_id=group_id, message=message)
        return
    message = game.retBoard

    await bot.send_group_msg(group_id=group_id, message=message)
    return

async def GetPic(bot: Bot, event: Event, game, group_id, user_id, text, message):
    img_path = os.path.split(os.path.realpath(__file__))[0] + '/resources/' + str(game.config) + '.jpg'
    print(img_path)
    await bot.send_group_msg(group_id=group_id, message=MessageSegment.image('file:///' + img_path))
    return


async def AddConfig(bot: Bot, event: Event, game, group_id, user_id, text, message):
    if game.config != 0:
        message = '[错误] 你只能在0模式下更改角色配置。请结束游戏，然后使用 [新游戏0] 创建游戏，再使用这个指令。'
        await bot.send_group_msg(group_id=group_id, message=message)
        return
    
    nums = []
    now, pos = 0, 0
    while now != -1:
        nums.append(now)
        now, pos = getNumber2(text, pos)
        
    if len(nums) < 5:
        message = '[错误] 数字数量不能小于4'
        await bot.send_group_msg(group_id=group_id, message=message)
        return
    nums[0] = nums[1] + nums[2] + nums[3] + nums[4]
    game.playerNum = [nums[0], nums[1], nums[2], nums[3], nums[4]]
    for i in range(5, len(nums)):
        game.expectIdentities.append(nums[i])
    
    message = '配置更改成功！'
    await bot.send_group_msg(group_id=group_id, message=message)
    return