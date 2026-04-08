# 在文件顶部添加导入
import random
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

from nonebot.log import logger

from ._read import *
import time
import asyncio

# 修改导入方式，避免循环导入
# 不要在顶层导入clear和getGame
# from src.plugins.Game import clear, getGame


startTimer = {}


alarm = on_keyword(['#alarm'],priority=40)
@alarm.handle()
async def alarm_handle(bot: Bot, event: Event):



    msg = event.get_session_id()
    if not ('group' in msg):
        return
    group_id = str(getNumber(event.get_session_id(), 0))
    text = event.get_plaintext()


    if '_show' in text or '_all' in text:
        message = '[ 闹钟列表 ]\n\n'
        global startTimer
        for i in startTimer:
            message += i + ' : ' + str(startTimer[i]) +'\n'
        await bot.send_group_msg(group_id=group_id, message=message)
        return


    await setAlarm(bot, event, group_id, text)
    await alarm.finish()
    return


async def setAlarm(bot: Bot, event: Event, group_id, text):
    group_id = str(getNumber(event.get_session_id(), 0))
    user_id = str(getNumber(event.get_session_id(), len(group_id) + 6))

    text = text
    num,p = getNumber2(text, 0)
    word = getString(text, p)

    message = "";

    global startTimer
    if (not group_id in startTimer):
        startTimer[group_id] = 0

    if "stop" in text:
        if startTimer[group_id] != 0:
            startTimer[group_id] = 0
            message = '⏰倒计时已被强制终止。'
            await bot.send_group_msg(group_id=group_id, message=message)
        return

    if(num < 10 or num > 3600):
        message = '[错误] 时间必须在 10 秒到 3600 秒之间。你所设定的是：' + str(num)
        await bot.send_group_msg(group_id=group_id, message=message)
        return 0

    if startTimer[group_id] != 0:
        message = '⏰上一个倒计时已被强制终止，将进入新的倒计时。\n\n'
    message += '⏰'+ word + ' ' + str(num) + ' 秒，倒计时开始。'
    await bot.send_group_msg(group_id=group_id, message=message)

    rem = time.time()
    startTimer[group_id] = rem

    if num > 3000:
        await reminder(bot, event, num, 3000, word, group_id, rem)
        num = 3000
    if num > 1200:
        await reminder(bot, event, num, 1200, word, group_id, rem)
        num = 1200
    if num > 300:
        await reminder(bot, event, num, 300, word, group_id, rem)
        num = 300
    if num > 120:
        await reminder(bot, event, num, 120, word, group_id, rem)
        num = 120
    if num > 50:
        await reminder(bot, event, num, 50, word, group_id, rem)
        num = 50
    if num > 20:
        await reminder(bot, event, num, 20, word, group_id, rem)
        num = 20
    if num > 5:
        await reminder(bot, event, num, 5, word, group_id, rem)
        num = 5
    if num > 0:
        await reminder(bot, event, num, 0, word, group_id, rem)
        num = 0

    if startTimer[group_id] == rem:
        startTimer[group_id] = 0
        message ='⏰'+ word + '计时结束。'
        await bot.send_group_msg(group_id = group_id, message = message)
        
        # 新增：倒计时结束时调用handle_alarm_end函数
        try:
            await handle_alarm_end(bot, event, group_id, word)
        except Exception as e:
            logger.error(f"处理倒计时结束事件时出错: {str(e)}")
        
        return 1

    return 0

async def handle_alarm_end(bot, event, group_id, alarm_type):
    # 延迟导入，避免循环导入问题
    from src.plugins.Game import clear, games, nightfall
    # 自己实现获取游戏实例的逻辑
    game = None
    for g in games:
        if g.group_id == group_id:
            game = g
            break
            
    if not game:
        return
    
    # 检查是否是官方模式
    is_advanced = hasattr(game, 'current_mode') and game.current_mode == "advanced"
    
    # 普通模式下的加时处理
    if not is_advanced:
        # 处理加时提名倒计时结束
        if alarm_type == "加时提名" and game.status == "picking":
            from src.plugins.Game import vote
            dm_user_id = game.DM[0]['user_id'] if game.DM and game.DM[0] else None
            if dm_user_id:
                await bot.send_group_msg(group_id=group_id, message="⏰ 加时提名结束，自动进入投票阶段")
                await vote(bot, event, group_id, dm_user_id, "#vote", "", game, auto_flow=True)
                # 设置投票倒计时
                await setAlarm(bot, event, group_id, "#alarm 120 投票")
            return
        
        # 处理加时投票倒计时结束
        if alarm_type == "加时投票" and game.status == "voting":
            from src.plugins.Game import clear
            dm_user_id = game.DM[0]['user_id'] if game.DM and game.DM[0] else None
            if dm_user_id:
                await bot.send_group_msg(group_id=group_id, message="⏰ 加时投票结束，自动结算投票")
                await clear(bot, event, group_id, dm_user_id, "#clear", "", game)
            return
        
        # 处理加时讨论倒计时结束
        if alarm_type == "加时讨论" and game.status == "started":
            from src.plugins.Game import pick, vote, clear
            dm_user_id = game.DM[0]['user_id'] if game.DM and game.DM[0] else None
            if dm_user_id:
                await bot.send_group_msg(group_id=group_id, message="⏰ 加时讨论结束，自动进入提名阶段")
                await pick(bot, event, group_id, dm_user_id, "#pick", "", game)
                await setAlarm(bot, event, group_id, "#alarm 120 提名")
                await vote(bot, event, group_id, dm_user_id, "#vote", "", game, auto_flow=True)
                await setAlarm(bot, event, group_id, "#alarm 120 投票")
                await clear(bot, event, group_id, dm_user_id, "#clear", "", game)
            return
        
        return
        
    # 如果是投票时间结束且在官方模式下
    if alarm_type == "投票时间" and game.status == "voting":
        # 顺时针投票模式下跳过自动结算
        if getattr(game, 'sequential_voting_enabled', False) and getattr(game, 'sequential_active', False):
            logger.info(f"群 {group_id} 顺时针投票进行中，跳过自动清算")
            return
        # 检查是否已经手动清算过投票
        # 如果游戏状态不再是voting，说明DM已经手动清算过了
        if game.status != "voting":
            logger.info(f"群 {group_id} 的投票已被手动清算，跳过自动清算")
            return
            
        # 自动执行clear命令
        await bot.send_group_msg(group_id=group_id, message="⏰ 投票时间结束，自动结算投票")
        
        # 获取DM的user_id
        dm_user_id = game.DM[0]['user_id'] if game.DM[0] else None
        if dm_user_id:
            # 创建一个模拟的clear命令事件
            # 确保使用DM的user_id来调用clear函数，这样才有权限
            await clear(bot, event, group_id, dm_user_id, "#clear", "", game)
            # 重置投票允许状态
            game.voting_allowed = False
    
    # 新增：处理提名阶段倒计时结束
    elif "提名阶段" in alarm_type and game.status == "picking":
        # 检查是否已经手动进入其他阶段
        if game.status != "picking":
            logger.info(f"群 {group_id} 的提名阶段已被手动结束，跳过自动入夜")
            return
            
        # 自动执行入夜命令
        await bot.send_group_msg(group_id=group_id, message="⏰ 提名阶段结束，自动执行入夜")
        
        # 获取DM的user_id
        dm_user_id = game.DM[0]['user_id'] if game.DM[0] else None
        if dm_user_id:
            # 调用night函数，模拟DM执行入夜指令
            await nightfall(bot, event, group_id, dm_user_id, "#入夜", "⏰ 自动执行：", game)
    # 顺时针投票回合的倒计时已移至Game.py中处理，不再使用Alarm插件
    # elif "顺时针投票回合" in alarm_type:
    #     from src.plugins.Game import games, advance_to_next_turn, clear
    #     game = None
    #     for g in games:
    #         if g.group_id == group_id:
    #             game = g
    #             break
    #     if not game:
    #         return
    #     if getattr(game, 'sequential_voting_enabled', False) and getattr(game, 'sequential_active', False) and game.status == "voting":
    #         # 若当前轮到被提名者则立即结算本次投票
    #         if getattr(game, 'current_turn_seat', 0) == getattr(game, 'sequential_nominee', 0):
    #             dm_user_id = game.DM[0]['user_id'] if game.DM and game.DM[0] else None
    #             await bot.send_group_msg(group_id=group_id, message="⏰ 被提名者超时未选择，立即结算投票")
    #             if dm_user_id:
    #                 await clear(bot, event, group_id, dm_user_id, "#clear", "", game)
    #             game.sequential_active = False
    #             game.voting_allowed = False
    #             await setAlarm(bot, event, group_id, "#alarm stop")
    #             return
    #         # 否则视为该玩家不投票，顺时针进入下一位
    #         seat = getattr(game, 'current_turn_seat', 0)
    #         name = ''
    #         if seat and seat - 1 >= 0 and seat - 1 < len(game.players):
    #             player = game.players[seat - 1]
    #             name = player['name'] if player else ''
    #         await bot.send_group_msg(group_id=group_id, message=f"⏰ {seat}号玩家（{name}）超时，自动视为放弃投票")
    #         await advance_to_next_turn(bot, event, group_id, game)

async def reminder(bot, event, t1, t2, word, group_id, T):

    group_id = str(getNumber(event.get_session_id(), 0))
    global startTimer
    await asyncio.sleep(t1 - t2)

    if startTimer[group_id] != T:
        return

    message = ''

    if t2 != 0:
        message ='⏰'+ word + '剩余'
        if t2 >= 60:
            message += ' ' + str(int(t2/60)) + ' 分钟'
            t2 = t2 % 60
        if t2 != 0:
            message += ' ' + str(int(t2)) + ' 秒'
        message += '。'
        await bot.send_group_msg(group_id = group_id, message = message)

    return