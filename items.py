"""
Items module for RPG Game
Defines all item types: Weapons, Armor, Consumables
Provides a scalable base for adding new item types
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from Character.Character_RPG import Character

# ==============================
# BASE ITEM CLASSES
# ==============================

class Item:
    """
    Base class for all items in the game
    
    Attributes:
        name (str): Display name of the item
        value (int): Gold/coin value of the item
    """
    
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', value={self.value})"


# ==============================
# WEAPON CLASS
# ==============================

class Weapon(Item):
    """
    Weapon items that increase player attack power
    
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
    
    def __repr__(self):
        return f"Weapon(name='{self.name}', type='{self.weapon_type}', damage={self.damage})"


# ==============================
# ARMOR CLASS
# ==============================

class Armor(Item):
    """
    Armor items that increase player defense
    
    Attributes:
        name (str): Armor name
        defense (int): Defense bonus
        defense_type (str|list): Type(s) of protection (Sharp, Blunt, Magic, etc.)
        value (int): Purchase/sell value
        rarity (str): Rarity tier
    """
    
    def __init__(self, name: str, defense: int, defense_type: Union[str, List[str]], value: int, rarity: str = "Common"):
        super().__init__(name, value)
        self.defense = defense
        self.defense_type = defense_type
        self.rarity = rarity
    
    def __repr__(self):
        return f"Armor(name='{self.name}', defense={self.defense})"


# ==============================
# CONSUMABLE INTERFACE
# ==============================

class Consumable(ABC):
    """
    Abstract base class for consumable items
    All consumables must implement the use() method
    """
    
    @abstractmethod
    def use(self, entity: 'Character') -> None:
        """
        Apply the consumable's effect to an entity
        
        Args:
            entity: The character/entity using the consumable
        """
        pass


# ==============================
# HEALTH POTION CLASS
# ==============================

class HealthPotion(Item, Consumable):
    """
    Health restoration potions
    
    Attributes:
        name (str): Potion name
        value (int): Purchase/sell value
        heals (int): HP restoration amount
    """
    
    def __init__(self, name: str, value: int, heals: int):
        super().__init__(name, value)
        self.heals = heals
    
    def use(self, entity: 'Character') -> None:
        """
        Heal the target entity
        
        Args:
            entity: Character to heal
        """
        old_hp = entity.hp
        entity.hp = min(entity.max_hp, entity.hp + self.heals)
        actual_heal = entity.hp - old_hp
        print(f"{entity.name} drank {self.name} and healed {actual_heal} HP (HP: {entity.hp}/{entity.max_hp})")


# ==============================
# PREDEFINED ITEMS
# ==============================

# Weapons
ShortSword = Weapon("Short Sword", "Sharp", 5, 10, "Common")
ShortBow = Weapon("Short Bow", "Ranged", 4, 8, "Common")
LongSword = Weapon("Long Sword", "Sharp", 12, 35, "Uncommon")
Mace = Weapon("Mace", "Blunt", 8, 25, "Common")

# Armor
WizardsRobe = Armor("Wizard's Robe", 2, "Magic", 10, "Common")
LeatherArmor = Armor("Leather Armor", 3, ["Sharp", "Blunt"], 5, "Common")
IronArmor = Armor("Iron Armor", 12, ["Sharp", "Blunt"], 50, "Rare")

# Potions
SmallHPotion = HealthPotion("Small Health Potion", 10, 25)
MediumHPotion = HealthPotion("Medium Health Potion", 20, 35)
LargeHPotion = HealthPotion("Large Health Potion", 30, 50)
XLHPotion = HealthPotion("XL Health Potion", 40, 80)