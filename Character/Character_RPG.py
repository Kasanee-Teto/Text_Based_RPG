"""
Character classes for RPG Game
Defines base Character class and Player class with all RPG mechanics
"""

from inventory import Inventory
from typing import Optional, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from items import Weapon, Armor
    from Character.Role import Role


# ==============================
# BASE CHARACTER CLASS
# ==============================

class Character:
    """
    Base class for all characters (players and enemies)
    
    Attributes:
        name (str): Character name
        hp (int): Current health points
        max_hp (int): Maximum health points
        attack_power (int): Base attack damage
        defense (int): Damage reduction
    """
    
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack
        self.defense = defense
    
    def is_alive(self) -> bool:
        """Check if character is still alive"""
        return self.hp > 0
    
    def take_damage(self, damage: int):
        """
        Reduce HP by damage amount (minimum 0)
        
        Args:
            damage: Amount of damage to take
        """
        self.hp -= max(0, damage)
        if self.hp < 0:
            self.hp = 0
    
    def defeated(self, entity):
        """
        Called when this character is defeated
        Override in subclasses for specific behavior
        """
        pass
    
    def attack(self, target: 'Character') -> int:
        """
        Perform basic attack on a target
        
        Args:
            target: Character being attacked
            
        Returns:
            int: Actual damage dealt
        """
        damage = max(0, self.attack_power - getattr(target, "defense", 0))
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")
        return damage


# ==============================
# PLAYER CLASS
# ==============================

class Player(Character):
    """
    Player character with inventory, leveling, equipment, and role systems
    
    Attributes:
        exp (int): Current experience points
        level (int): Current level
        exp_needed (int): EXP required for next level
        role (Role): Chosen character role/class
        status_effects (list): Active status effects
        equipped_weapon (Weapon): Currently equipped weapon
        equipped_armor (Armor): Currently equipped armor
        inventory (Inventory): Player's item storage
        coins (int): Currency for shops
    """
    
    def __init__(self, name: str, start_hp: int = 100, start_attack: int = 8, 
                 start_defense: int = 2, start_coins: int = 200):
        """
        Initialize a new player character
        
        Args:
            name: Player's name
            start_hp: Starting health
            start_attack: Starting attack power
            start_defense: Starting defense
            start_coins: Starting currency
        """
        super().__init__(name, hp=start_hp, attack=start_attack, defense=start_defense)
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.role: Optional['Role'] = None
        self. status_effects = []
        self.equipped_weapon: Optional['Weapon'] = None
        self.equipped_armor: Optional['Armor'] = None
        self. inventory = Inventory()
        self.coins = start_coins
    
    def gain_exp(self, amount: int):
        """
        Add experience points and trigger level ups
        
        Args:
            amount: EXP to gain
        """
        self.exp += amount
        self.level_up()
    
    def level_up(self):
        """
        Check for level ups and apply stat increases
        Automatically levels up multiple times if enough EXP
        """
        while self.exp >= self.exp_needed:
            self.level += 1
            self.max_hp += 20
            self.hp = min(self.max_hp, self.hp + 20)  # Heal on level up
            self.attack_power += 5
            self.defense += 2
            self.exp -= self. exp_needed
            self.exp_needed += int(self.level * math.sqrt(self.exp_needed))
            print(f"🎉 {self.name} leveled up!  Now level {self.level}.")
            
            if self.level == 5 and self.role is None:
                print(f"{self.name} can now choose a role (Warrior, Mage, Archer, Healer)!")
    
    def choose_role(self, role: 'Role'):
        """
        Assign a role/class to the player (level 5+ only)
        
        Args:
            role: Role class instance to assign
        """
        if self.level >= 5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
            print(f"{self.name} became a {role.name}!")
        else:
            print("Can't select role yet!  Must be level 5 with no current role.")
    
    def equip_weapon(self, weapon: 'Weapon'):
        """
        Equip a weapon from inventory
        Swaps with current weapon if one is equipped
        
        Args:
            weapon: Weapon item to equip
        """
        if weapon not in self.inventory. items:
            print("Weapon not in inventory!")
            return
        
        if self.equipped_weapon is None:
            print(f"{self.name} equipped {weapon.name}")
            self.inventory.remove_item(weapon)
            self.equipped_weapon = weapon
            self.attack_power += getattr(weapon, "damage", 0)
        else:
            print(f"{self.name} swapped {self.equipped_weapon.name} with {weapon.name}")
            self.attack_power -= getattr(self.equipped_weapon, "damage", 0)
            self.inventory.add_item(self.equipped_weapon)
            self.inventory.remove_item(weapon)
            self.equipped_weapon = weapon
            self.attack_power += getattr(weapon, "damage", 0)
    
    def equip_armor(self, armor: 'Armor'):
        """
        Equip armor from inventory
        Swaps with current armor if one is equipped
        
        Args:
            armor: Armor item to equip
        """
        if armor not in self.inventory.items:
            print("Armor not in inventory!")
            return
        
        if self.equipped_armor is None:
            print(f"{self.name} equipped {armor.name}")
            self.inventory.remove_item(armor)
            self.equipped_armor = armor
            self. defense += getattr(armor, "defense", 0)
        else:
            print(f"{self.name} swapped {self. equipped_armor.name} with {armor.name}")
            self. defense -= getattr(self.equipped_armor, "defense", 0)
            self.inventory.add_item(self.equipped_armor)
            self.inventory.remove_item(armor)
            self.equipped_armor = armor
            self.defense += getattr(armor, "defense", 0)
    
    def defeated(self, enemy):
        """Handle player defeat - clear status effects"""
        self.status_effects = []
        print(f"💀 {enemy.name} has killed {self.name}!  Come back when you are stronger!")
    
    def update_status_effects(self):
        """Apply damage and debuffs from active status effects"""
        # Bleeding effects
        if "bleeding" in self.status_effects:
            bleed_damage = 3
            self.hp = max(0, self.hp - bleed_damage)
            print(f"🩸 {self.name} suffers from bleeding and loses {bleed_damage} HP.")
        elif "bleeding_demon" in self.status_effects:
            bleed_damage_demon = 5
            self. hp = max(0, self. hp - bleed_damage_demon)
            print(f"🩸 {self.name} suffers from severe bleeding and loses {bleed_damage_demon} HP.")
        
        # Weakened effects
        if "weakened" in self.status_effects:
            weakened_atk = max(1, int(self.attack_power * 0.8))
            weakened_def = max(1, int(self.defense * 0.8))
            print(f"💢 {self.name} is weakened!  ATK {self.attack_power}→{weakened_atk}, DEF {self.defense}→{weakened_def}")
            self.attack_power = weakened_atk
            self. defense = weakened_def
        elif "weakened_demon" in self.status_effects:
            weakened_atk_demon = max(1, int(self.attack_power * 0.6))
            weakened_def_demon = max(1, int(self.defense * 0.6))
            print(f"💢 {self.name} is severely weakened! ATK {self. attack_power}→{weakened_atk_demon}, DEF {self.defense}→{weakened_def_demon}")
            self.attack_power = weakened_atk_demon
            self.defense = weakened_def_demon
    
    def get_stats_display(self) -> dict:
        """
        Get formatted stats for display
        
        Returns:
            dict: Dictionary of all player stats
        """
        return {
            'name': self.name,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack_power,
            'defense': self.defense,
            'level': self.level,
            'exp': f"{self.exp}/{self.exp_needed}",
            'coins': self.coins,
            'weapon': self.equipped_weapon.name if self.equipped_weapon else "Unarmed",
            'armor': self.equipped_armor.name if self.equipped_armor else "Unarmored",
            'role': self.role.name if self.role else "None",
            'status_effects': self.status_effects
        }