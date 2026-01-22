"""
Abstract Factory implementation for RPG characters.
Converted from direct instantiation to an Abstract Factory pattern
without changing responsibilities or behaviors.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, List
import math
from inventory import Inventory
from config import CONFIG

if TYPE_CHECKING:
    from items import Weapon, Armor
    from Character.Role import RoleStrategy

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
        return self.hp > 0
    
    def take_damage(self, damage: int):
        self.hp -= max(0, damage)
        if self.hp < 0:
            self.hp = 0
    
    def defeated(self, entity):
        """Called when this character is defeated. Override in subclasses."""
        pass
    
    def attack(self, target: "Character") -> int:
        """Perform basic attack on a target"""
        damage = max(0, self.attack_power - getattr(target, "defense", 0))
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")
        return damage

class Player(Character):
    """
    Player character with inventory, leveling, equipment, and role systems
    """
        super().__init__(name, hp=start_hp, attack=start_attack, defense=start_defense)
        self.exp = CONFIG.PLAYER.START_EXP
        self.level = CONFIG.PLAYER.START_LEVEL
        self.exp_needed = CONFIG.PLAYER.BASE_EXP_NEEDED
        self.role: Optional["RoleStrategy"] = None
        self.status_effects: List[str] = []
        self.equipped_weapon: Optional["Weapon"] = None
        self.equipped_armor: Optional["Armor"] = None
        self.inventory = Inventory()
        self.coins = start_coins
        self._original_attack: Optional[int] = None
        self._original_defense: Optional[int] = None
        self.crit_rate: float = 0.0
    
    def gain_exp(self, amount: int):
        self.exp += amount
        self.level_up()
    
    def level_up(self):
        while self.exp >= self.exp_needed:
            self.level += 1
            self.max_hp += CONFIG.PLAYER.LEVEL_UP_HP_BONUS
            self.hp = min(self.max_hp, self.hp + CONFIG.PLAYER.LEVEL_UP_HP_BONUS)
            self.attack_power += CONFIG.PLAYER.LEVEL_UP_ATTACK_BONUS
            self.defense += CONFIG.PLAYER.LEVEL_UP_DEFENSE_BONUS
            self.exp -= self.exp_needed
            self.exp_needed += int(self.level * math.sqrt(self.exp_needed))
            print(f"🎉 {self.name} leveled up! Now level {self.level}.")
            
            if self.level == CONFIG.PLAYER.ROLE_UNLOCK_LEVEL and self.role is None:
                print(f"{self.name} can now choose a role!")
    
    def choose_role(self, role: "RoleStrategy"):
        if self.level >= CONFIG.PLAYER.ROLE_UNLOCK_LEVEL and self.role is None:
            self.role = role
            role.apply_bonus(self)
            print(f"{self.name} became a {role.__class__.__name__}!")
        else:
            print("Can't select role yet!  Must be level 5 with no current role.")
    
    # --- Equipment ---
    def equip_weapon(self, weapon: "Weapon"):
        if weapon not in self.inventory.items:
            print("Weapon not in inventory!")
            return
        if self.equipped_weapon:
            print(f"{self.name} swapped {self.equipped_weapon.name} with {weapon.name}")
            self.attack_power -= self.equipped_weapon.damage
            self.inventory.add_item(self.equipped_weapon)
        else:
            print(f"{self.name} equipped {weapon.name}")
            
        self.inventory.remove_item(weapon)
        self.equipped_weapon = weapon
        self.attack_power += weapon.damage
    
    def equip_armor(self, armor: "Armor"):
        if armor not in self.inventory.items:
            print("Armor not in inventory!")
            return
        if self.equipped_armor:
            print(f"{self.name} swapped {self.equipped_armor.name} with {armor.name}")
            self.defense -= self.equipped_armor.defense
            self.inventory.add_item(self.equipped_armor)
        else:
            print(f"{self.name} equipped {armor.name}")
            
        self.inventory.remove_item(armor)
        self.equipped_armor = armor
        self.defense += armor.defense

    def defeated(self, enemy):
        self._reset_temp_stats()
        self.status_effects = []
        print(f"💀 {enemy.name} has killed {self.name}! Come back when you are stronger!")
    
    def _reset_temp_stats(self):
        if self._original_attack is not None:
            self.attack_power = self._original_attack
            self._original_attack = None
        if self._original_defense is not None:
            self.defense = self._original_defense
            self._original_defense = None

    def update_status_effects(self):
        self._reset_temp_stats()
        
        if "bleeding" in self.status_effects:
            self._apply_bleed(CONFIG.STATUS.BLEED_DAMAGE)
        elif "bleeding_demon" in self.status_effects:
            self._apply_bleed(CONFIG.STATUS.BLEED_DAMAGE_DEMON, "severely")
        
        if "weakened" in self.status_effects:
            self._apply_weaken(CONFIG.STATUS.WEAKENED_MULTIPLIER)
        elif "weakened_demon" in self.status_effects:
            self._apply_weaken(CONFIG.STATUS.WEAKENED_DEMON_MULTIPLIER, "severely")

    def _apply_bleed(self, amount: int, severity: str = ""):
        self.hp = max(0, self.hp - amount)
        desc = f"suffers from {severity} bleeding" if severity else "suffers from bleeding"
        print(f"🩸 {self.name} {desc} and loses {amount} HP.")

    def _apply_weaken(self, multiplier: float, severity: str = ""):
        self._original_attack = self.attack_power
        self._original_defense = self.defense
        new_atk = max(1, int(self.attack_power * multiplier))
        new_def = max(1, int(self.defense * multiplier))
        desc = f"is {severity} weakened" if severity else "is weakened"
        print(f"💢 {self.name} {desc}! ATK {self.attack_power}→{new_atk}, DEF {self.defense}→{new_def}")
        self.attack_power = new_atk
        self.defense = new_def

    def get_stats_display(self) -> dict:
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack_power,
            "defense": self.defense,
            "level": self.level,
            "exp": f"{self.exp}/{self.exp_needed}",
            "coins": self.coins,
            "weapon": self.equipped_weapon.name if self.equipped_weapon else "Unarmed",
            "armor": self.equipped_armor.name if self.equipped_armor else "Unarmored",
            "role": self.role.__class__.__name__ if self.role else "None",
            "status_effects": self.status_effects,
        }



class CharacterFactory(ABC):
    """Abstract Factory for creating RPG characters."""
    
    @abstractmethod
    def create_character(self, name: str, hp: int, attack: int, defense: int) -> Character:
        """Create a non-player character (enemy, NPC, etc.)."""
        raise NotImplementedError
    
    @abstractmethod
    def create_player(
        self,
        name: str,
        start_hp: int = 100,
        start_attack: int = 8,
        start_defense: int = 2,
        start_coins: int = 200,
    ) -> Player:
        """Create a player character."""
        raise NotImplementedError


class DefaultRPGFactory(CharacterFactory):
    """
    Default concrete factory producing Character and Player instances.
    Extend or subclass this factory to customize creation logic
    (e.g., inject starting gear, roles, or difficulty scaling).
    """
    def create_character(self, name: str, hp: int, attack: int, defense: int) -> Character:
        return Character(name=name, hp=hp, attack=attack, defense=defense)
    
    def create_player(
        self,
        name: str,
        start_hp: int = 100,
        start_attack: int = 8,
        start_defense: int = 2,
        start_coins: int = 200,
    ) -> Player:
        return Player(
            name=name,
            start_hp=start_hp,
            start_attack=start_attack,
            start_defense=start_defense,
            start_coins=start_coins,
        )

