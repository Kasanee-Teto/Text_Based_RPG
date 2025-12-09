"""
Role Strategy System for Text-Based RPG
=======================================

This module implements the Strategy Pattern for character roles/classes.
Each role is represented as a separate strategy class, responsible for 
applying unique stat bonuses to a player.

Design Pattern:
---------------
Strategy Pattern — each role encapsulates its own bonus logic, and 
the Player class dynamically selects a role strategy at runtime.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Character.Character_RPG import Player
# ==============================
# BASE ROLE CLASS
# ==============================

class RoleStrategy(ABC):
    @abstractmethod
    def apply_bonus(self, player):
        pass

# class Role:
    """
    Base class for character roles/classes
    
    Attributes:
        name (str): Role name
        bonus_attack (int): Attack bonus when role is selected
        bonus_defense (int): Defense bonus when role is selected
        bonus_hp (int): Max HP bonus when role is selected
    """

# ===============================================================================================

# ==============================
# ROLE SUBCLASSES
# ==============================

# class Warrior

# ==============================
# ROLE SUBCLASSES
# ==============================
# Class Warrior

#     """
#     Tank role with high defense and HP
#     Best for absorbing damage in prolonged fights
#     """


class WarriorStrategy(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 3
        player.defense += 5
        player.hp += 30
        print(f"{player.name} chose Warrior! (+3 ATK, +5 DEF, +30 HP)")


# ======================================================================================================
# class Mage
#     """
#     High damage, low defense glass cannon
#     Maximum offensive power at cost of survivability
#     """
#

class MageStrategy(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 10
        player.defense -= 2
        print(f"{player.name} chose Mage! (+10 ATK, -2 DEF)")


# ======================================================================================================


# class Archer
#     """
#     Balanced ranged fighter
#     Good mix of attack and survivability
#     """


class ArcherStrategy(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 7
        player.defense += 2
        player.hp += 10
        print(f"{player.name} chose Archer! (+7 ATK, +2 DEF, +10 HP)")

# =====================================================================================
# class Assassin
#     """
#     High-burst melee specialist
#     Excels in critical strikes and fast damage output,
#     but sacrifices defense and durability for agility and offensive power.
#     Ideal for players who prefer aggressive, high-risk combat strategies.
#     """
class AssassinStrategy(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 12    
        player.defense -= 3            
        player.hp += 5                 
        player.crit_rate += 0.15      
        
        print(f"{player.name} chose Assassin! (+12 ATK, -3 DEF, +5 HP, +15% CRIT Chance)")

# =====================================================================================

# class Healer
#     """
#     Support role with modest bonuses
#     Could be extended with healing abilities
#     """
class HealerStrategy(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 2
        player.defense += 3
        player.hp += 15
        print(f"{player.name} chose Healer! (+2 ATK, +3 DEF, +15 HP)")

    def heal(self, target):
        heal_amount = 20
        target.hp += heal_amount
        print(f"Healer restores {heal_amount} HP to {target.name}.")