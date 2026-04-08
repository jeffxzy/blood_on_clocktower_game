#!/usr/bin/env python3
import sys
import os
import random

# Set working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

print("=" * 60)
print("       Blood on the Clocktower - Game Simulation Test")
print("=" * 60)
print()

# Step 1: Read and prepare all necessary modules
print(">>> Loading game modules...")

# 1. Load _read.py
with open(os.path.join(current_dir, '_read.py'), 'r', encoding='utf-8') as f:
    read_content = f.read()
exec(read_content, globals())
print("  [OK] _read.py loaded")

# 2. Load Rand.py
with open(os.path.join(current_dir, 'Rand.py'), 'r', encoding='utf-8') as f:
    rand_content = f.read()
exec(rand_content, globals())
print("  [OK] Rand.py loaded")

# 3. Load modules from identities/
identities_dir = os.path.join(current_dir, 'identities')

# First, load TownsfolkClass.py
with open(os.path.join(identities_dir, 'townsfolks', 'TownsfolkClass.py'), 'r', encoding='utf-8') as f:
    townsfolk_class_content = f.read()
townsfolk_class_content = townsfolk_class_content.replace('from ..IdentityClass import *', '')
exec(townsfolk_class_content, globals())
print("  [OK] TownsfolkClass.py loaded")

# Load OutsiderClass.py
with open(os.path.join(identities_dir, 'outsiders', 'OutsiderClass.py'), 'r', encoding='utf-8') as f:
    outsider_class_content = f.read()
outsider_class_content = outsider_class_content.replace('from ..IdentityClass import *', '')
exec(outsider_class_content, globals())
print("  [OK] OutsiderClass.py loaded")

# Load MinionClass.py
with open(os.path.join(identities_dir, 'minions', 'MinionClass.py'), 'r', encoding='utf-8') as f:
    minion_class_content = f.read()
minion_class_content = minion_class_content.replace('from ..IdentityClass import *', '')
exec(minion_class_content, globals())
print("  [OK] MinionClass.py loaded")

# Load DemonClass.py
with open(os.path.join(identities_dir, 'demons', 'DemonClass.py'), 'r', encoding='utf-8') as f:
    demon_class_content = f.read()
demon_class_content = demon_class_content.replace('from ..IdentityClass import *', '')
exec(demon_class_content, globals())
print("  [OK] DemonClass.py loaded")

# Load townsfolks/_Nobody.py
with open(os.path.join(identities_dir, 'townsfolks', '_Nobody.py'), 'r', encoding='utf-8') as f:
    nobody_content = f.read()
nobody_content = nobody_content.replace('from .TownsfolkClass import *', '')
exec(nobody_content, globals())
print("  [OK] _Nobody.py loaded")

# Load IdentityClass.py
with open(os.path.join(identities_dir, 'IdentityClass.py'), 'r', encoding='utf-8') as f:
    identity_class_content = f.read()
identity_class_content = identity_class_content.replace('import copy', 'import copy\nimport sys\nimport os')
exec(identity_class_content, globals())
print("  [OK] IdentityClass.py loaded")

# Load all role files
role_files = []
for root, dirs, files in os.walk(identities_dir):
    for file in files:
        if file.endswith('.py') and file != '__init__.py' and file != 'IdentityClass.py' and file != 'ImportIdentities.py':
            role_files.append(os.path.join(root, file))

for role_file in role_files:
    try:
        with open(role_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove all relative imports
        content = content.replace('from .TownsfolkClass import *', '')
        content = content.replace('from .OutsiderClass import *', '')
        content = content.replace('from .MinionClass import *', '')
        content = content.replace('from .DemonClass import *', '')
        content = content.replace('from ..IdentityClass import *', '')
        exec(content, globals())
    except Exception as e:
        pass
print(f"  [OK] {len(role_files)} role files loaded")

# Load ImportIdentities.py
with open(os.path.join(identities_dir, 'ImportIdentities.py'), 'r', encoding='utf-8') as f:
    import_identities_content = f.read()
# Remove all relative imports
import_identities_content = import_identities_content.replace('from .townsfolks.', '')
import_identities_content = import_identities_content.replace('from .outsiders.', '')
import_identities_content = import_identities_content.replace('from .minions.', '')
import_identities_content = import_identities_content.replace('from .demons.', '')
import_identities_content = import_identities_content.replace('from .townsfolks', '')
import_identities_content = import_identities_content.replace('from .outsiders', '')
import_identities_content = import_identities_content.replace('from .minions', '')
import_identities_content = import_identities_content.replace('from .demons', '')
exec(import_identities_content, globals())
print("  [OK] ImportIdentities.py loaded")

# Load GameClass.py
with open(os.path.join(current_dir, 'GameClass.py'), 'r', encoding='utf-8') as f:
    game_class_content = f.read()
game_class_content = game_class_content.replace('from ._read import *', '')
game_class_content = game_class_content.replace('from .Alarm import *', '')
game_class_content = game_class_content.replace('from .Rand import *', '')
game_class_content = game_class_content.replace('from .identities.IdentityClass import *', '')
game_class_content = game_class_content.replace('from .identities.ImportIdentities import *', '')
exec(game_class_content, globals())
print("  [OK] GameClass.py loaded")

print()
print(">>> Starting game simulation...")
print()

# Create game
game = Game()
game.group_id = "test_simulation_001"
game.config = 1
game.status = "init"
print("[OK] Game created successfully")

# Initialize game
game.init()

if game.status == "stop":
    print(f"[ERROR] Game init failed: {game.retBoard}")
    sys.exit(1)

print(f"[OK] Game initialized")
print(f"  Setup: {game.cName}")
print(f"  Players: {game.playerNum[0]}")
print()

# Display player info
print("-" * 40)
print("Player List:")
print("-" * 40)
for i in range(1, game.playerNum[0] + 1):
    player = game.players[i]
    role_type_display = {
        'townsfolk': 'Townsfolk',
        'outsider': 'Outsider',
        'minion': 'Minion',
        'demon': 'Demon'
    }.get(player.type, 'Unknown')
    alignment = "Good" if player.good == 1 else "Evil"
    marker = "[GOOD]" if player.good == 1 else "[EVIL]"
    print(f"  {marker} Player {i}: {player.name} ({role_type_display}, {alignment})")

print()
print("-" * 40)
print("Starting game flow...")
print("-" * 40)
print()

# Day 1
print(">>> Day 1 (First Night)")
game.day()
print(f"[OK] Day 1 ended, current status: {game.status}")
print()

# Simulate execution
print(">>> Finding and executing the demon...")
demon_seat = -1
for i in range(1, game.playerNum[0] + 1):
    if game.players[i].type == 'demon' and game.players[i].alive == 1:
        demon_seat = i
        break

if demon_seat != -1:
    print(f"  Found demon at seat {demon_seat}")
    game.players[demon_seat].killed(game)
    game.allBoard += f"Player {demon_seat} was executed\n"
    
    game.gameEndCheck()
    
    if game.status == "stop":
        print()
        print("=" * 60)
        print("                  GAME OVER!")
        print("=" * 60)
        if "善良获胜" in game.allBoard:
            print("              Good Team Wins!")
        elif "邪恶获胜" in game.allBoard:
            print("              Evil Team Wins!")
        print("=" * 60)
else:
    print("  No alive demon found")

print()
print("=" * 60)
print("              Complete Game Record")
print("=" * 60)
print(game.allBoard)
print()
print("=" * 60)
print("              Test Complete!")
print("=" * 60)
