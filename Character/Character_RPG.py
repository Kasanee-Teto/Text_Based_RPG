"""
Character module dengan penerapan prinsip SOLID:
- SRP: Pisah tanggung jawab status effect handler dan equipment handler.
- OCP: Status effect & role bonus berbasis registry/mapping.
- LSP: Subclass Character (Player/Enemy) mempertahankan kontrak.
- ISP: Interface kecil untuk efek/status.
- DIP: Dependensi Inventory bisa di-inject.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Optional, TYPE_CHECKING, Protocol
import math
from inventory import Inventory

if TYPE_CHECKING:
    from items import Weapon, Armor
    from Role import RoleStrategy

# ------------------------------
# Protocols / Interfaces (ISP)
# ------------------------------

class StatusEffectApplier(Protocol):
    def apply(self, player: "Player") -> None: ...


class RoleStrategy(Protocol):
    def apply_bonus(self, player: "Player") -> None: ...


# ------------------------------
# Domain Models
# ------------------------------

class Character:
    """
    Base class untuk semua karakter (SRP: status dasar & aksi dasar).
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
        """Override di subclass bila perlu."""
        pass

    def attack(self, target: "Character") -> int:
        damage = max(0, self.attack_power - getattr(target, "defense", 0))
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")
        return damage


@dataclass(frozen=True)
class RoleBonus:
    attack: int = 0
    defense: int = 0
    hp: int = 0
    crit_rate: float = 0.0


class Player(Character):
    """
    Player dengan leveling, equipment, status effect, dan role (SRP: core state & public API).
    """
    def __init__(
        self,
        name: str,
        start_hp: int = 100,
        start_attack: int = 8,
        start_defense: int = 2,
        start_coins: int = 200,
        inventory_factory: Callable[[], Inventory] = Inventory,
    ):
        super().__init__(name, hp=start_hp, attack=start_attack, defense=start_defense)
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.current_depth = 1
        self.role: Optional[RoleStrategy] = None
        self.status_effects: list[str] = []
        self.applied_status_effects: set[str] = set()
        self.equipped_weapon: Optional["Weapon"] = None
        self.equipped_armor: Optional["Armor"] = None
        self.inventory = inventory_factory()
        self.coins = start_coins
        self._original_attack = None
        self._original_defense = None
        self.crit_rate: float = 0.0

        # Registries
        self._status_registry: Dict[str, Callable[[], None]] = {
            "bleeding": self._apply_bleeding,
            "bleeding_demon": self._apply_bleeding_demon,
            "weakened": self._apply_weakened,
            "weakened_demon": self._apply_weakened_demon,
        }

    # ---------------- Leveling ----------------
    def gain_exp(self, amount: int):
        self.exp += amount
        self.level_up()

    def level_up(self):
        while self.exp >= self.exp_needed:
            self.level += 1
            self.max_hp += 20
            self.hp = min(self.max_hp, self.hp + 20)
            self.attack_power += 5
            self.defense += 2
            self.exp -= self.exp_needed
            self.exp_needed += int(self.level * math.sqrt(self.exp_needed))
            print(f"🎉 {self.name} leveled up!  Now level {self.level}.")
            if self.level == 5 and self.role is None:
                print(f"{self.name} can now choose a role (Warrior, Mage, Archer, Healer, Assassin)!")

    def choose_role(self, role: RoleStrategy):
        if self.level >= 5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
            print(f"{self.name} became a {role.__class__.__name__}!")
        else:
            print("Can't select role yet!  Must be level 5 with no current role.")

    # ---------------- Equipment ----------------
    def equip_weapon(self, weapon: "Weapon"):
        if weapon not in self.inventory.items:
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

    def equip_armor(self, armor: "Armor"):
        if armor not in self.inventory.items:
            print("Armor not in inventory!")
            return
        if self.equipped_armor is None:
            print(f"{self.name} equipped {armor.name}")
            self.inventory.remove_item(armor)
            self.equipped_armor = armor
            self.defense += getattr(armor, "defense", 0)
        else:
            print(f"{self.name} swapped {self.equipped_armor.name} with {armor.name}")
            self.defense -= getattr(self.equipped_armor, "defense", 0)
            self.inventory.add_item(self.equipped_armor)
            self.inventory.remove_item(armor)
            self.equipped_armor = armor
            self.defense += getattr(armor, "defense", 0)

    # ---------------- Combat outcomes ----------------
    def defeated(self, enemy):
        self.cleanup_status_effects()
        print(f"💀 {enemy.name} has killed {self.name}!  Come back when you are stronger!")

    def cleanup_status_effects(self):
        """Removes all status effects and restores original stats."""
        if self._original_attack is not None:
            self.attack_power = self._original_attack
            self._original_attack = None
        if self._original_defense is not None:
            self.defense = self._original_defense
            self._original_defense = None
        self.status_effects = []
        self.applied_status_effects = set()

    def update_status_effects(self):
        for effect in list(self.status_effects):
            if effect not in self.applied_status_effects:
                handler = self._status_registry.get(effect)
                if handler:
                    handler()
                    self.applied_status_effects.add(effect)

    # ---------------- Status effect handlers ----------------
    def _apply_bleeding(self):
        bleed_damage = 3
        self.hp = max(0, self.hp - bleed_damage)
        print(f"🩸 {self.name} suffers from bleeding and loses {bleed_damage} HP.")

    def _apply_bleeding_demon(self):
        bleed_damage_demon = 5
        self.hp = max(0, self.hp - bleed_damage_demon)
        print(f"🩸 {self.name} suffers from severe bleeding and loses {bleed_damage_demon} HP.")

    def _apply_weakened(self):
        if self._original_attack is None: self._original_attack = self.attack_power
        if self._original_defense is None: self._original_defense = self.defense
        
        weakened_atk = max(1, int(self._original_attack * 0.8))
        weakened_def = max(1, int(self._original_defense * 0.8))
        print(f"💢 {self.name} is weakened!  ATK {self.attack_power}→{weakened_atk}, DEF {self.defense}→{weakened_def}")
        self.attack_power = weakened_atk
        self.defense = weakened_def

    def _apply_weakened_demon(self):
        if self._original_attack is None: self._original_attack = self.attack_power
        if self._original_defense is None: self._original_defense = self.defense

        weakened_atk_demon = max(1, int(self._original_attack * 0.6))
        weakened_def_demon = max(1, int(self._original_defense * 0.6))
        print(f"💢 {self.name} is severely weakened! ATK {self.attack_power}���{weakened_atk_demon}, DEF {self.defense}→{weakened_def_demon}")
        self.attack_power = weakened_atk_demon
        self.defense = weakened_def_demon

    # ---------------- UI helpers ----------------
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
            "crit_rate": getattr(self, "crit_rate", 0.0),
        }

# ... (Factories remain unchanged) ...
class CharacterFactory(ABC):
    @abstractmethod
    def create_character(self, name: str, hp: int, attack: int, defense: int) -> Character: ...
    @abstractmethod
    def create_player(self, name: str, start_hp: int = 100, start_attack: int = 8, start_defense: int = 2, start_coins: int = 200) -> Player: ...

class DefaultRPGFactory(CharacterFactory):
    def create_character(self, name: str, hp: int, attack: int, defense: int) -> Character:
        return Character(name=name, hp=hp, attack=attack, defense=defense)
    def create_player(self, name: str, start_hp: int = 100, start_attack: int = 8, start_defense: int = 2, start_coins: int = 200) -> Player:
        return Player(name=name, start_hp=start_hp, start_attack=start_attack, start_defense=start_defense, start_coins=start_coins)