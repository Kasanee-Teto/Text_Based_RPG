"""
Configuration file for RPG Game
Centralizes all game constants and settings for easy modification and scalability
W.I.P
"""

# ==============================
# GAME BALANCE SETTINGS
# ==============================

class GameConfig:
    """Central configuration for game balance and settings"""
    
    # Player starting stats
    PLAYER_START_HP = 100
    PLAYER_START_ATTACK = 8
    PLAYER_START_DEFENSE = 2
    PLAYER_START_COINS = 200
    PLAYER_START_LEVEL = 1
    PLAYER_START_EXP = 0
    PLAYER_BASE_EXP_NEEDED = 100
    
    # Level up bonuses
    LEVEL_UP_HP_BONUS = 20
    LEVEL_UP_ATTACK_BONUS = 5
    LEVEL_UP_DEFENSE_BONUS = 2
    ROLE_UNLOCK_LEVEL = 5
    
    # Status effect values
    BLEED_DAMAGE = 3
    BLEED_DAMAGE_DEMON = 5
    WEAKENED_MULTIPLIER = 0.8
    WEAKENED_DEMON_MULTIPLIER = 0.6
    
    # Drop chances
    NORMAL_DROP_CHANCE = 0.5
    BOSS_DROP_CHANCE = 0.8
    FINAL_BOSS_DROP_CHANCE = 0.7
    
    # Shop settings
    SELL_PRICE_MULTIPLIER = 0.5
    
    # Dungeon settings
    DEFAULT_DUNGEON_WIDTH = 5
    DEFAULT_DUNGEON_HEIGHT = 5
    DUNGEON_ENEMY_SPAWN_RATE = 0.45
    DUNGEON_TREASURE_SPAWN_RATE = 0.25
    DUNGEON_TRAP_SPAWN_RATE = 0.10
    DUNGEON_BOSS_SPAWN_RATE = 0.25
    DUNGEON_DEMON_SPAWN_RATE = 0.15
    
    # UI Settings
    SEPARATOR_LENGTH = 50
    LOADING_DELAY_MIN = 0.2
    LOADING_DELAY_MAX = 0.5


# ==============================
# ENEMY STATS DATABASE
# ==============================

class EnemyStats:
    """Database of enemy statistics for easy balancing"""
    
    ENEMIES = {
        'spider': {'hp': 15, 'attack': 5, 'defense': 1, 'exp': 10},
        'goblin': {'hp': 45, 'attack': 10, 'defense': 2, 'exp': 15},
        'skeleton': {'hp': 30, 'attack': 10, 'defense': 2, 'exp': 11},
        'zombie': {'hp': 35, 'attack': 10, 'defense': 2, 'exp': 13},
    }
    
    BOSSES = {
        'wolf': {'hp': 75, 'attack': 20, 'defense': 5, 'exp': 25},
        'ogre': {'hp': 80, 'attack': 15, 'defense': 5, 'exp': 30},
        'vampire': {'hp': 65, 'attack': 30, 'defense': 5, 'exp': 35},
        'demon': {'hp': 100, 'attack': 30, 'defense': 3, 'exp': 50},
    }