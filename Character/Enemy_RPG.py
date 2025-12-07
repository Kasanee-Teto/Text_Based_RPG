"""
Enemy classes for RPG Game
Defines all enemy types with unique behaviors and abilities
"""

from Character.Character_RPG import Character
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Character.Character_RPG import Player


# ==============================
# BASE ENEMY CLASS
# ==============================

class Enemy(Character):
    """
    Base class for all enemies
    
    Attributes:
        exp_reward (int): EXP given to player on defeat
        defeated_count (int): Times this enemy type has been defeated
    """
    
    def __init__(self, name: str, hp: int, attack: int, defense: int, exp_reward: int):
        super().__init__(name, hp, attack, defense)
        self. exp_reward = exp_reward
        self.defeated_count = 0
    
    def scale_difficulty(self, factor: float = 1.0) -> dict:
        """
        Scale enemy stats by difficulty factor
        
        Args:
            factor: Multiplier for stats (1.0 = normal, 1.5 = 50% harder)
            
        Returns:
            dict: Scaled stats
        """
        return {
            "hp": int(self.max_hp * factor),
            "attack": int(self.attack_power * factor),
            "defense": int(self.defense * factor)
        }
    
    def defeated(self, player: 'Player'):
        """
        Handle enemy defeat - award EXP to player
        
        Args:
            player: The victorious player
        """
        self.defeated_count += 1
        player.exp += self.exp_reward
        print(f"🏆 {self.name} defeated! {player.name} wins!")
        print(f"💫 {player.name} gained {self.exp_reward} EXP\n")


# ==============================
# NORMAL ENEMIES
# ==============================

class goblin(Enemy):
    """Basic goblin enemy - balanced stats"""
    def __init__(self):
        super().__init__("Goblin", 45, 10, 2, 15)


class spider(Enemy):
    """Weak but fast spider enemy - low HP, low attack"""
    def __init__(self):
        super().__init__("Spider", 15, 5, 1, 10)


class skeleton(Enemy):
    """Undead skeleton - moderate stats"""
    def __init__(self):
        super().__init__("Skeleton", 30, 10, 2, 11)


class zombie(Enemy):
    """Slow zombie - slightly higher HP than skeleton"""
    def __init__(self):
        super().__init__("Zombie", 35, 10, 2, 13)


# ==============================
# BOSS ENEMIES
# ==============================

class Wolf(Enemy):
    """
    Boss enemy with bleeding attack
    Inflicts 'bleeding' status effect on hit
    """
    def __init__(self):
        super().__init__("Alpha Wolf", 75, 20, 5, 25)
    
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"🩸 {target.name} is bleeding!")


class Ogre(Enemy):
    """
    Boss enemy with weakening attack
    Inflicts 'weakened' status effect, reducing target stats
    """
    def __init__(self):
        super().__init__("Ogre Brute", 80, 15, 5, 30)
    
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"💢 {target.name}'s stats are temporarily reduced (weakened)!")


class Vampire(Enemy):
    """
    Boss enemy with life drain
    Heals for 30% of attack damage dealt
    """
    def __init__(self):
        super().__init__("Vampire Lord", 65, 30, 5, 35)
    
    def attack(self, target):
        damage = super().attack(target)
        heal = int(damage * 0.3)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"🧛 {self.name} drains blood!  HP recovered {heal} (HP: {self.hp}/{self. max_hp})")


# ==============================
# FINAL BOSS
# ==============================

class Demon(Enemy):
    """
    Final boss with multiple debilitating effects
    - Inflicts severe bleeding
    - Inflicts severe weakening
    - Life drains 50% of damage
    """
    def __init__(self):
        super().__init__("Demon King", 100, 30, 3, 50)
    
    def attack(self, target):
        damage = super().attack(target)
        
        # Apply severe bleeding
        target.status_effects.append("bleeding_demon")
        print(f"🩸 {target.name} is severely bleeding!")
        
        # Apply severe weakening
        target.status_effects.append("weakened_demon")
        print(f"💢 {target.name}'s stats are severely reduced!")
        
        # Life drain
        heal = int(damage * 0.5)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"😈 {self.name} drains life force and restores {heal} HP!")