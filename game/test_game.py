import unittest
import sys
import os

# 获取当前文件所在目录和项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))

# 把项目根目录加入 sys.path，这样我们可以用包导入方式
sys.path.insert(0, project_root)

# 现在直接用包导入方式导入所需模块
# 这样相对导入就可以正常工作了
from src.plugins.blood_on_clocktower_game.game.GameClass import Game


class TestGame(unittest.TestCase):
    def test_normal_game_simulation(self):
        """测试一场正常的对局模拟"""
        print("=" * 50)
        print("开始测试正常对局模拟")
        print("=" * 50)

        # 1. 创建游戏实例
        game = Game()
        game.group_id = "test_group_123"
        game.config = 1  # 使用标准1板子（8人局）
        game.status = "init"

        self.assertEqual(game.status, "init")
        print(f"[OK] 游戏创建成功，板子: {game.config}")

        # 2. 初始化游戏
        game.init()

        self.assertNotEqual(game.status, "stop")
        self.assertTrue(len(game.players) > 0)
        self.assertEqual(game.playerNum[0], 8)  # 8人局
        print(f"[OK] 游戏初始化完成，玩家数: {game.playerNum[0]}")

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
        self.assertEqual(game.days, 1)
        self.assertEqual(game.status, "day")
        print(f"\n[OK] 第1天结束，天数: {game.days}, 状态: {game.status}")

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
            self.assertEqual(game.status, "stop")
            self.assertIn("善良获胜", game.allBoard)
            print("[OK] 游戏结束 - 善良阵营获胜！")
        else:
            print("[WARN] 未找到存活的恶魔，跳过处决测试")

        # 7. 打印完整的游戏记录摘要（避免 Unicode 编码错误）
        print("\n" + "=" * 50)
        print("完整游戏记录:")
        print("=" * 50)
        print("(游戏记录包含特殊字符，已省略打印)")

        print("\n" + "=" * 50)
        print("测试通过！")
        print("=" * 50)

    def test_evil_victory_simulation(self):
        """测试邪恶阵营获胜的情况"""
        print("\n" + "=" * 50)
        print("开始测试邪恶阵营获胜模拟")
        print("=" * 50)

        # 创建游戏实例
        game = Game()
        game.group_id = "test_group_456"
        game.config = 1  # 使用标准1板子（8人局）
        game.status = "init"

        # 初始化游戏
        game.init()
        game.day()  # 先执行一天，进入白天

        # 模拟处决多个好人，直到存活人数≤2
        print("\n开始模拟处决好人...")
        target_seats = []
        for i in range(1, game.playerNum[0] + 1):
            if game.players[i].good == 1 and game.players[i].alive == 1:
                target_seats.append(i)

        # 处决足够多的好人 - 8人游戏，需要处决到存活≤2
        # 初始8人，处决6个好人剩下2人（一个恶魔和一个好人）
        for seat in target_seats[:6]:
            game.players[seat].killed(game)
            game.allBoard += f"{seat}号被处决\n"

        # 检查游戏是否结束（邪恶获胜）
        game.gameEndCheck()
        self.assertEqual(game.status, "stop")
        self.assertIn("邪恶获胜", game.allBoard)
        print("[OK] 游戏结束 - 邪恶阵营获胜！")

        print("\n完整游戏记录:")
        print("(游戏记录包含特殊字符，已省略打印)")
        print("\n测试通过！")


if __name__ == '__main__':
    unittest.main()
