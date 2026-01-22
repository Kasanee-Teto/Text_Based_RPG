"""
Items module for RPG Game
Defines all item types: Weapons, Armor, Consumables
Provides a scalable base for adding new item types
Refactor to follow Open-Closed Principle
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Character.Character_RPG import Character

# ==============================
# BASE ITEM CLASSES
# ==============================

class Items(ABC):
    """
    Abstract base class for all items in the game
    Open for extension, closed for modification

    Attributes:
        name (str): Display name of the item
        value (int): Gold/coin value of the item
    """
    
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', value={self.value})"
    
    def get_description(self) -> str:
        """Get item description - can be overridden by subclasses"""
        return f"{self.name} (Value: {self.value} coins)"


# ==============================
# WEAPON CLASS
# ==============================

class Weapon(Items):
    """
    Weapon items that increase player attack power
    Open for extension through subclassing
    
    Attributes:
        name (str): Weapon name
        weapon_type (str): Type category (Sharp, Blunt, Ranged, etc.)
        damage (int): Attack power bonus
        value (int): Purchase/sell value
        rarity (str): Rarity tier (Common, Uncommon, Rare, Epic, Legendary)
    """
    
    def __init__(self, name: str, weapon_type: str, damage: int, value: int, rarity: str = "Common"):
        super().__init__(name, value)
        self.weapon_type = weapon_type
        self.damage = damage
        self.rarity = rarity
    
    def get_damage(self) -> int:
        """Get weapon damage - can be overridden for special weapons"""
        return self.damage
    
    def get_description(self) -> str:
        """Get weapon description - can be overridden by subclasses"""
        return f"{self.name} [{self.rarity}] - {self.weapon_type} weapon, Damage: {self.damage}"
    
    def __repr__(self):
        return f"Weapon(name='{self.name}', type='{self.weapon_type}', damage={self.damage})"


# ==============================
# ARMOR CLASS
# ==============================

class Armor(Items):
    """
    Armor items that increase player defense
    Open for extension through subclassing
    
    Attributes:
        name (str): Armor name
        defense (int): Defense bonus
        defense_type (str|list): Type(s) of protection (Sharp, Blunt, Magic, etc.)
        value (int): Purchase/sell value
        rarity (str): Rarity tier
    """
    
    def __init__(self, name: str, defense: int, defense_type, value: int, rarity: str = "Common"):
        super().__init__(name, value)
        self.defense = defense
        self.defense_type = defense_type
        self.rarity = rarity
    
    def get_defense(self) -> int:
        """Get armor defense - can be overridden for special armor"""
        return self.defense
    
    def get_description(self) -> str:
        """Get armor description - can be overridden by subclasses"""
        return f"{self.name} [{self.rarity}] - Defense: {self.defense}"
    
    def __repr__(self):
        return f"Armor(name='{self.name}', defense={self.defense})"


# ==============================
# CONSUMABLE INTERFACE
# ==============================

class Consumable(ABC):
    """
    Abstract base class for consumable items
    All consumables must implement the uses() method
    """
    
    @abstractmethod
    def uses(self, entity: 'Character'):
        """
        Apply the consumable's effect to an entity
        
        Args:
            entity: The character/entity using the consumable
        """
        pass


# ==============================
# HEALTH POTION CLASS
# ==============================

class Health_Potions(Items, Consumable):
    """
    Health restoration potions
    Open for extension through subclassing
    
    Attributes:
        name (str): Potion name
        value (int): Purchase/sell value
        heals (int): HP restoration amount
    """
    
    def __init__(self, name: str, value: int, heals: int):
        super().__init__(name, value)
        self.heals = heals
    
    def calculate_healing(self, entity: 'Character') -> int:
        """Calculate healing amount - can be overridden for special potions"""
        return self.heals
    
    def apply_healing(self, entity: 'Character', heal_amount: int):
        """Apply healing to entity - can be extended for additional effects"""
        old_hp = entity.hp
        entity.hp = min(entity.max_hp, entity.hp + heal_amount)
        actual_heal = entity.hp - old_hp
        print(f"{entity.name} drank {self.name} and healed {actual_heal} HP (HP: {entity.hp}/{entity.max_hp})")
    
    def uses(self, entity: 'Character'):
        """
        Heal the target entity using template method pattern
        
        Args:
            entity: Character to heal
        """
        heal_amount = self.calculate_healing(entity)
        self.apply_healing(entity, heal_amount)
    
    def get_description(self) -> str:
        """Get potion description - can be overridden by subclasses"""
        return f"{self.name} - Restores {self.heals} HP"


# ==============================
# PREDEFINED ITEMS
# ==============================

# Weapons
Short_Sword = Weapon("Short Sword", "Sharp", 5, 10, "Common")
Short_bow = Weapon("Short Bow", "Ranged", 4, 8, "Common")
Long_Sword = Weapon("Long Sword", "Sharp", 12, 35, "Uncommon")
Mace = Weapon("Mace", "Blunt", 8, 25, "Common")

# Armor
Wizards_Robe = Armor("Wizard's Robe", 2, "Magic", 10, "Common")
Leather_Armor = Armor("Leather Armor", 3, ["Sharp", "Blunt"], 5, "Common")
Iron_Armor = Armor("Iron Armor", 12, ["Sharp", "Blunt"], 50, "Rare")

# Potions
Small_HPotion = Health_Potions("Small Health Potion", 10, 25)
Medium_HPotion = Health_Potions("Medium Health Potion", 20, 35)
Large_HPotion = Health_Potions("Large Health Potion", 30, 50)
XL_HPotion = Health_Potions("XL Health Potion", 40, 80)