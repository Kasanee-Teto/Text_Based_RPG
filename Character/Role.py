"""
Role/Class system for RPG Game
Defines character roles with unique stat bonuses
W.I.P: Extendable for special abilities per role
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
    
    # def __init__(self, name: str, bonus_attack: int = 0, bonus_defense: int = 0, bonus_hp: int = 0):
    #     self.name = name
    #     self.bonus_attack = bonus_attack
    #     self.bonus_defense = bonus_defense
    #     self.bonus_hp = bonus_hp
    
    # def apply_bonus(self, player: 'Player'):
    #     """
    #     Apply role bonuses to a player
        
    #     Args:
    #         player: Player receiving the bonuses
    #     """
    #     player.attack_power += self.bonus_attack
    #     player.defense += self.bonus_defense
    #     player.max_hp += self.bonus_hp
    #     player.hp += self.bonus_hp
    #     print(f"✨ {player.name} chose the {self.name} role!")
    #     print(f"   Bonuses: +{self.bonus_attack} ATK, +{self.bonus_defense} DEF, +{self.bonus_hp} HP")
# ===============================================================================================

# ==============================
# ROLE SUBCLASSES
# ==============================

# class Warrior(Role):
#     """
#     Tank role with high defense and HP
#     Best for absorbing damage in prolonged fights
#     """
#     def __init__(self):
#         super().__init__("Warrior", bonus_attack=3, bonus_defense=5, bonus_hp=30)

class Warrior(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 3
        player.defense += 5
        player.hp += 30
        print(f"{player.name} chose Warrior! (+3 ATK, +5 DEF, +30 HP)")


# ======================================================================================================

# class Mage(Role):
#     """
#     High damage, low defense glass cannon
#     Maximum offensive power at cost of survivability
#     """
#     def __init__(self):
#         super().__init__("Mage", bonus_attack=10, bonus_defense=-2, bonus_hp=0)

class Mage(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 10
        player.defense -= 2
        print(f"{player.name} chose Mage! (+10 ATK, -2 DEF)")


# ======================================================================================================


# class Archer(Role):
#     """
#     Balanced ranged fighter
#     Good mix of attack and survivability
#     """
#     def __init__(self):
        # super().__init__("Archer", bonus_attack=7, bonus_defense=2, bonus_hp=10)

class Archer(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 7
        player.defense += 2
        player.hp += 10
        print(f"{player.name} chose Archer! (+7 ATK, +2 DEF, +10 HP)")


# =====================================================================================
class Assassin(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 12    
        player.defense -= 3            
        player.hp += 5                 
        player.crit_rate += 0.15      
        
        print(f"{player.name} chose Assassin! (+12 ATK, -3 DEF, +5 HP, +15% CRIT Chance)")

# =====================================================================================

# class Healer(Role):
#     """
#     Support role with modest bonuses
#     Could be extended with healing abilities
#     """
#     def __init__(self):
#         super().__init__("Healer", bonus_attack=2, bonus_defense=3, bonus_hp=15)
    
#     def heal(self, target: 'Player', amount: int = 20):
#         """
#         Heal a target (special healer ability - not yet integrated)
        
#         Args:
#             target: Character to heal
#             amount: HP to restore
#         """
#         old_hp = target.hp
#         target.hp = min(target. max_hp, target.hp + amount)
#         actual_heal = target.hp - old_hp
#         print(f"💚 {self.name} used Heal! {target.name} recovered {actual_heal} HP.")

class Healer(RoleStrategy):
    def apply_bonus(self, player):
        player.attack_power += 2
        player.defense += 3
        player.hp += 15
        print(f"{player.name} chose Healer! (+2 ATK, +3 DEF, +15 HP)")

    def heal(self, target):
        heal_amount = 20
        target.hp += heal_amount
        print(f"Healer restores {heal_amount} HP to {target.name}.")