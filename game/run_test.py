import sys
import os

# 设置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 临时修改导入方式 - 创建一个包装模块
import importlib.util

def import_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# 导入所有依赖模块
import_from_file('_read', os.path.join(current_dir, '_read.py'))
import_from_file('Rand', os.path.join(current_dir, 'Rand.py'))
import_from_file('Alarm', os.path.join(current_dir, 'Alarm.py'))

# 导入身份相关模块
identities_dir = os.path.join(current_dir, 'identities')
sys.path.insert(0, identities_dir)

# 先导入 IdentityClass
identity_class_content = ''
with open(os.path.join(identities_dir, 'IdentityClass.py'), 'r', encoding='utf-8') as f:
    identity_class_content = f.read()

# 临时修改导入并执行
identity_class_content = identity_class_content.replace('import copy', 'import copy\nimport sys\nimport os')
exec(identity_class_content, globals())

# 现在导入 GameClass
game_class_content = ''
with open(os.path.join(current_dir, 'GameClass.py'), 'r', encoding='utf-8') as f:
    game_class_content = f.read()

# 修改相对导入为绝对导入
game_class_content = game_class_content.replace('from ._read import *', 'from _read import *')
game_class_content = game_class_content.replace('from .Alarm import *', 'from Alarm import *')
game_class_content = game_class_content.replace('from .Rand import *', 'from Rand import *')
game_class_content = game_class_content.replace('from .identities.IdentityClass import *', '')
game_class_content = game_class_content.replace('from .identities.ImportIdentities import *', '')

# 执行 GameClass
exec(game_class_content, globals())

# 导入 ImportIdentities
import_identities_content = ''
with open(os.path.join(identities_dir, 'ImportIdentities.py'), 'r', encoding='utf-8') as f:
    import_identities_content = f.read()

# 执行 ImportIdentities
exec(import_identities_content, globals())

print("=" * 50)
print("开始测试正常对局模拟")
print("=" * 50)

# 1. 创建游戏实例
game = Game()
game.group_id = "test_group_123"
game.config = 1  # 使用标准1板子（8人局）
game.status = "init"

print(f"✓ 游戏创建成功，板子: {game.config}")

# 2. 初始化游戏
game.init()

if game.status == "stop":
    print(f"✗ 游戏初始化失败: {game.retBoard}")
    sys.exit(1)

print(f"✓ 游戏初始化完成，玩家数: {game.playerNum[0]}")

# 3. 打印玩家身份信息
print("\n玩家列表:")
for i in range(1, game.playerNum[0] + 1):
    player = game.players[i]
    alignment = "善良" if player.good == 1 else "邪恶"
    role_type = {
        'townsfolk': '镇民',
        'outsider': '外来者',
        'minion': '爪牙',
        'demon': '恶魔'
    }.get(player.type, '未知')
    print(f"  {i}号: {player.name} ({role_type}, {alignment})")

# 4. 进入第一天（首夜）
game.day()
print(f"\n✓ 第1天结束，天数: {game.days}, 状态: {game.status}")

# 5. 模拟处决恶魔（让善良阵营获胜）
demon_seat = -1
for i in range(1, game.playerNum[0] + 1):
    if game.players[i].type == 'demon' and game.players[i].alive == 1:
        demon_seat = i
        break

if demon_seat != -1:
    print(f"\n发现恶魔在 {demon_seat} 号座位，模拟处决...")
    game.players[demon_seat].killed(game)
    game.allBoard += f"{demon_seat}号被处决\n"

    # 6. 检查游戏是否结束（善良获胜）
    game.gameEndCheck()
    if game.status == "stop" and "善良获胜" in game.allBoard:
        print("✓ 游戏结束 - 善良阵营获胜！")
    else:
        print("⚠ 游戏状态异常")
else:
    print("⚠ 未找到存活的恶魔，跳过处决测试")

# 7. 打印完整的游戏记录
print("\n" + "=" * 50)
print("完整游戏记录:")
print("=" * 50)
print(game.allBoard)

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)
