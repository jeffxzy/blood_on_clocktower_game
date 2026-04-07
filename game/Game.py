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
from src.plugins.game.GameProcess import *


games = []
# 注册指令监听器 - 使用 # 作为前缀触发游戏指令
GameMessage = on_keyword(['.'], priority=50)
@GameMessage.handle()
async def GameMessage_handle(bot: Bot, event: Event):
    group_id = str(getNumber(event.get_session_id(), 0))
    user_id = str(getNumber(event.get_session_id(), len(group_id) + 6))
    text = event.get_plaintext()
    message = ''
    
    await solveGame(bot, event, group_id, user_id, text, message)
    await GameMessage.finish()


async def solveGame(bot: Bot, event :Event, group_id, user_id, text, message):

    if 'test' in text or '测试' in text:
        await testGame(bot, event, group_id, user_id, text, message)
        return
    if '新游戏' in text or 'new' in text or 'init' in text:
        await newGame(bot, event, group_id, user_id, text, message)
        return
    if '加入' in text or 'join' in text:
        await joinGame(bot, event, group_id, user_id, text, message)
        return
    if '退出' in text or 'quit' in text:
        await quitGame(bot, event, group_id, user_id, text, message)
        return
    if '状态' in text or 'status' in text or 'show' in text:
        await showGame(bot, event, group_id, user_id, text, message)
        return
    if '停止' in text or '结束' in text or '终止' in text or 'stop' in text:
        await stopGame(bot, event, group_id, user_id, text, message)
        return
    if '帮助' in text or 'help' in text:
        await help(bot, event, group_id, user_id, text, message)
        return
    if '%全部游戏' in text or '%allgame' in text:
        await showAllGame(bot, event, group_id, user_id, text, message)
        return

    for i in games:
        if i.group_id == group_id:
            for j in i.users:
                if j.user_id == user_id:
                    await ProcessGame(bot, event, i, group_id, user_id, text, message)
                    return
            # message = '[错误] 你未加入游戏。'
            # await bot.send_group_msg(group_id=group_id, message=message)
            return

    # message = '[错误] 指令不正确或本群不存在游戏。'
    # await bot.send_group_msg(group_id=group_id, message=message)
    return



async def testGame(bot: Bot, event: Event, group_id, user_id, text, message):

    global games
    for i in games:
        if i.group_id == group_id:
            game = i
    message = game.allBoard
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def newGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games
    for i in range(0, len(games)):
        if games[i].group_id == group_id:
            if games[i].status != 'stop':
                message = '[错误] 该房间已开始游戏。'
                await bot.send_group_msg(group_id=group_id, message=message)
                return
            else:
                del(games[i])
                break

    num = getNumber(text, 0)

    game = Game()
    game.group_id = group_id
    game.config = num
    game.status = 'init'
    games.append(game)

    await joinGame(bot, event, group_id, user_id, 'join房主', message)

    message = '创建游戏成功，您已默认加入游戏。现在玩家可以发送指令加入游戏。当前可选板子：0 - ' + str(game.maxConfig)
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def joinGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games
    for i in games:
        if i.group_id == group_id:
            for j in i.users:
                if j.user_id == user_id:
                    message = '[错误] 你已经加入本场游戏。'
                    await bot.send_group_msg(group_id=group_id, message=message)
                    return

    if '加入' in text:
        pos = text.index('加入') + len('加入')
    elif 'join' in text:
        pos = text.index('join') + len('join')
    name = getString(text, pos)

    for i in range(0, len(games)):
        if games[i].group_id == group_id:
            user = User()
            user.name = name
            user.user_id = user_id
            games[i].users.append(user)
            message = '加入成功。当前游戏人数：' + str(len(games[i].users))
            await bot.send_group_msg(group_id=group_id, message=message)
            return

    message = '[错误] 本群未找到游戏。'
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def quitGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games
    for i in range(0, len(games)):
        if games[i].group_id == group_id:
            for j in range(0, len(games[i].users)):

                if games[i].users[j].user_id == user_id:
                    del(games[i].users[j])
                    message = '退出成功。'
                    await bot.send_group_msg(group_id=group_id, message=message)

                    if len(games[i].users) == 0:
                        del(games[i])
                        message = '所有玩家退出了游戏，游戏解散。'
                        await bot.send_group_msg(group_id=group_id, message=message)

                    return

            message = '[错误] 未加入过游戏。'
            await bot.send_group_msg(group_id=group_id, message=message)
            return
    message = '[错误] 本群尚未存在游戏，请先创建新游戏。'
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def showGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games
    for i in range(0, len(games)):
        if games[i].group_id == group_id:

            message += '[玩家列表]\n'
            for j in range(0, len(games[i].users)):
                message += '\n' + str(j + 1)
                message += games[i].users[j].name + ' ('
                message += games[i].users[j].user_id + ')'
            await bot.send_group_msg(group_id=group_id, message=message)
            return

    message = '[错误] 本群没有正在进行中的游戏。'
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def stopGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games

    if "强制" in text:
        for i in range(0, len(games)):
            if games[i].group_id == group_id:
                del(games[i])
                message = '游戏强制解散成功。'
                await bot.send_group_msg(group_id=group_id, message=message)
                return
        message = '[错误] 本群没有正在进行中的游戏。'
        await bot.send_group_msg(group_id=group_id, message=message)
        return
    
    for i in range(0, len(games)):
        if games[i].group_id == group_id:
            if games[i].status == 'started' or  games[i].status == 'day' or  games[i].status == 'night':
                message = games[i].allBoard
                await bot.send_group_msg(group_id=group_id, message=message)
            del(games[i])
            message = '游戏解散成功。'
            await bot.send_group_msg(group_id=group_id, message=message)
            return

    message = '[错误] 本群没有正在进行中的游戏。'
    await bot.send_group_msg(group_id=group_id, message=message)
    return


async def pic(bot: Bot, event: Event, group_id, user_id, text, message):
    img_path = os.path.split(os.path.realpath(__file__))[0] + '/resources/1.jpg'
    await bot.send_group_msg(group_id=group_id, message=MessageSegment.image('file:///' + img_path))
    return

async def help(bot: Bot, event: Event, group_id, user_id, text, message):
    message = '[指令列表]\n\n' \
              '新游戏：创建新游戏\n' \
              '加入：加入游戏\n' \
              '退出：退出游戏\n' \
              '状态：查看玩家列表和游戏状态\n' \
              '停止：结束游戏\n\n' \
              '你必须加入游戏才能使用下面的指令：\n' \
              '开始：开始游戏\n' \
              '设置：设置游戏配置\n' \
              '处决：处决一名游戏内角色\n\n' \
              '在新游戏指令后方加入数字可游玩不同配置。加入0可自定义角色。'
    await bot.send_group_msg(group_id=group_id, message=message)
    return





async def showAllGame(bot: Bot, event: Event, group_id, user_id, text, message):
    global games
    message = '   [全部游戏列表]\n'
    for i in range(0, len(games)):
        message += '\n\n' + str(group_id) + '\n'
        message += '玩家列表：'
        for j in range(0, len(games[i].users)):
            message += '\n'
            message += games[i].users[j].name + ' '
            message += games[i].users[j].user_id + ' '

    await bot.send_group_msg(group_id=group_id, message=message)
    return