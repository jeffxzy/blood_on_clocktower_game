#!/usr/bin/env python3
import sys
import os

# 设置正确的路径和包结构
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.dirname(os.path.dirname(parent_dir))

sys.path.insert(0, src_dir)
sys.path.insert(0, parent_dir)

# 修改工作目录
os.chdir(current_dir)

# 设置包名，让相对导入能工作
__package__ = 'blood_on_clocktower_game.game'

# 现在导入我们需要的模块
try:
    from .GameClass import Game
    from ._read import *
    from .Alarm import *
    from .Rand import *
    from .identities.IdentityClass import *
    from .identities.ImportIdentities import *
except Exception as e:
    print(f"导入错误: {e}")
    print("尝试使用替代方法...")
    
    # 如果相对导入失败，使用动态导入的方法
    import importlib.util
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    
    # 加载所有需要的模块
    load_module('_read', os.path.join(current_dir, '_read.py'))
    load_module('Rand', os.path.join(current_dir, 'Rand.py'))
    load_module('Alarm', os.path.join(current_dir, 'Alarm.py'))
    
    # 修改 GameClass.py 的导入并加载
    game_class_path = os.path.join(current_dir, 'GameClass.py')
    with open(game_class_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('from ._read import *', 'from _read import *')
    content = content.replace('from .Alarm import *', 'from Alarm import *')
    content = content.replace('from .Rand import *', 'from Rand import *')
    content = content.replace('from .identities.IdentityClass import *', '')
    content = content.replace('from .identities.ImportIdentities import *', '')
    
    # 加载 IdentityClass
    identity_class_path = os.path.join(current_dir, 'identities', 'IdentityClass.py')
    with open(identity_class_path, 'r', encoding='utf-8') as f:
        identity_content = f.read()
    exec(identity_content, globals())
    
    # 加载 ImportIdentities
    import_identities_path = os.path.join(current_dir, 'identities', 'ImportIdentities.py')
    with open(import_identities_path, 'r', encoding='utf-8') as f:
        import_content = f.read()
    exec(import_content, globals())
    
    # 加载 GameClass
    exec(content, globals())

print("=" * 60)
print("                  血染钟楼游戏测试")
print("=" * 60)
print()

# 创建游戏
print(">>> 创建游戏实例...")
game = Game()
game.group_id = "test_12345"
game.config = 2  # 使用利维坦1板子
game.status = "init"
print("✓ 游戏创建成功")
print()

# 初始化游戏
print(">>> 初始化游戏...")
game.init()

if game.status == "stop":
    print(f"✗ 初始化失败: {game.retBoard}")
    sys.exit(1)

print(f"✓ 游戏初始化完成")
print(f"  - 板子: {game.cName}")
print(f"  - 玩家数: {game.playerNum[0]}")
print(f"  - 镇民: {game.playerNum[1]}")
print(f"  - 外来者: {game.playerNum[2]}")
print(f"  - 爪牙: {game.playerNum[3]}")
print(f"  - 恶魔: {game.playerNum[4]}")
print()

# 显示玩家
print(">>> 玩家列表:")
print("-" * 40)
for i in range(1, game.playerNum[0] + 1):
    player = game.players[i]
    role_type_map = {
        'townsfolk': '镇民',
        'outsider': '外来者',
        'minion': '爪牙',
        'demon': '恶魔'
    }
    role_type = role_type_map.get(player.type, '未知')
    alignment = "善良" if player.good == 1 else "邪恶"
    alive = "存活" if player.alive == 1 else "死亡"
    print(f"  {i}号: {player.name} ({role_type}, {alignment})")
print()

# 第一天
print(">>> 进入第1天...")
game.day()
print(f"✓ 第1天结束")
print(f"  - 天数: {game.days}")
print(f"  - 状态: {game.status}")
print()

# 模拟处决恶魔
print(">>> 寻找并处决恶魔...")
demon_seat = -1
for i in range(1, game.playerNum[0] + 1):
    if game.players[i].type == 'demon' and game.players[i].alive == 1:
        demon_seat = i
        break

if demon_seat != -1:
    print(f"  发现恶魔在 {demon_seat} 号座位")
    game.players[demon_seat].killed(game)
    game.allBoard += f"{demon_seat}号被处决\n"
    
    # 检查游戏结束
    game.gameEndCheck()
    
    if game.status == "stop":
        print("✓ 游戏结束!")
        if "善良获胜" in game.allBoard:
            print("  🎉 善良阵营获胜!")
        elif "邪恶获胜" in game.allBoard:
            print("  🎉 邪恶阵营获胜!")
else:
    print("  未找到存活的恶魔")

print()
print("=" * 60)
print("                  完整游戏记录")
print("=" * 60)
print(game.allBoard)
print()
print("=" * 60)
print("                  测试完成!")
print("=" * 60)
