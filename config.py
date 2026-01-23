"""
Configuration file for RPG Game.
Centralizes all game constants and settings.
"""
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class PlayerConfig:
    START_HP: int = 100
    START_ATTACK: int = 8
    START_DEFENSE: int = 2
    START_COINS: int = 200
    START_LEVEL: int = 1
    START_EXP: int = 0
    BASE_EXP_NEEDED: int = 100
    LEVEL_UP_HP_BONUS: int = 20
    LEVEL_UP_ATTACK_BONUS: int = 5
    LEVEL_UP_DEFENSE_BONUS: int = 2
    ROLE_UNLOCK_LEVEL: int = 5

@dataclass(frozen=True)
class StatusEffectConfig:
    BLEED_DAMAGE: int = 3
    BLEED_DAMAGE_DEMON: int = 5
    WEAKENED_MULTIPLIER: float = 0.8
    WEAKENED_DEMON_MULTIPLIER: float = 0.6

@dataclass(frozen=True)
class DungeonConfig:
    DEFAULT_WIDTH: int = 5
    DEFAULT_HEIGHT: int = 5
    DEFAULT_DEPTH: int = 1
    # Spawn rates (sum should ideally not exceed 1.0 for the logic, 
    # though logic will prioritize order: Enemy > Treasure > Trap)
    SPAWN_RATE_ENEMY: float = 0.45
    SPAWN_RATE_TREASURE: float = 0.25
    SPAWN_RATE_TRAP: float = 0.10
    
    # Conditional spawn rates
    SPAWN_RATE_DEMON: float = 0.15  # On deep floors
    SPAWN_RATE_BOSS: float = 0.25   # At exit

@dataclass(frozen=True)
class UIConfig:
    SEPARATOR_LENGTH: int = 50
    LOADING_DELAY_MIN: float = 0.2
    LOADING_DELAY_MAX: float = 0.5
    MSG_INVALID_CHOICE: str = "❌ Invalid choice!"
    MSG_INVALID_INPUT: str = "❌ Invalid input!"
    MSG_CREATE_CHAR_FIRST: str = "⚠️  Create a character first!"
    MSG_INVENTORY_EMPTY: str = "📦 Inventory is empty!"

@dataclass(frozen=True)
class GameConfig:
    PLAYER: PlayerConfig = PlayerConfig()
    STATUS: StatusEffectConfig = StatusEffectConfig()
    DUNGEON: DungeonConfig = DungeonConfig()
    UI: UIConfig = UIConfig()
    
    # Drop chances
    DROP_CHANCE_NORMAL: float = 0.5
    DROP_CHANCE_BOSS: float = 0.8
    DROP_CHANCE_FINAL_BOSS: float = 1
    
    # Shop
    SELL_PRICE_MULTIPLIER: float = 0.5

# Global instance for access
CONFIG = GameConfig()

# Enemy Stats Database
ENEMY_STATS: Dict[str, Dict[str, int]] = {
    'spider': {'hp': 15, 'attack': 5, 'defense': 1, 'exp': 10},
    'goblin': {'hp': 45, 'attack': 10, 'defense': 2, 'exp': 15},
    'skeleton': {'hp': 30, 'attack': 10, 'defense': 2, 'exp': 11},
    'zombie': {'hp': 35, 'attack': 10, 'defense': 2, 'exp': 13},
}

BOSS_STATS: Dict[str, Dict[str, int]] = {
    'wolf': {'hp': 75, 'attack': 20, 'defense': 5, 'exp': 25},
    'ogre': {'hp': 80, 'attack': 15, 'defense': 5, 'exp': 30},
    'vampire': {'hp': 65, 'attack': 30, 'defense': 5, 'exp': 35},
    'demon': {'hp': 100, 'attack': 30, 'defense': 3, 'exp': 50},
}