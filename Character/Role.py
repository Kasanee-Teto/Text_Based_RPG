"""
Role system with SOLID:
- SRP: Setiap role hanya mengurus bonusnya.
- OCP: Tambah role baru cukup tambah subclass RoleStrategy.
- LSP: Semua RoleStrategy dapat menggantikan RoleStrategy lain.
- ISP: Interface tunggal apply_bonus.
- DIP: Player tergantung pada abstraksi RoleStrategy, bukan konkret.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Character.Character_RPG import Player

# Base interface
class RoleStrategy(ABC):
    @abstractmethod
    def apply_bonus(self, player: "Player"):
        ...


# Role implementations (pertahankan nama kelas agar main.py tetap jalan)
class Warrior(RoleStrategy):
    def apply_bonus(self, player: "Player"):
        player.attack_power += 3
        player.defense += 5
        player.hp += 30
        print(f"{player.name} chose Warrior! (+3 ATK, +5 DEF, +30 HP)")


class Mage(RoleStrategy):
    def apply_bonus(self, player: "Player"):
        player.attack_power += 10
        player.defense -= 2
        print(f"{player.name} chose Mage! (+10 ATK, -2 DEF)")


class Archer(RoleStrategy):
    def apply_bonus(self, player: "Player"):
        player.attack_power += 7
        player.defense += 2
        player.hp += 10
        print(f"{player.name} chose Archer! (+7 ATK, +2 DEF, +10 HP)")


class Assassin(RoleStrategy):
    def apply_bonus(self, player: "Player"):
        player.attack_power += 12
        player.defense -= 3
        player.hp += 5
        player.crit_rate += 0.15
        print(f"{player.name} chose Assassin! (+12 ATK, -3 DEF, +5 HP, +15% CRIT Chance)")


class Healer(RoleStrategy):
    def apply_bonus(self, player: "Player"):
        player.attack_power += 2
        player.defense += 3
        player.hp += 15
        print(f"{player.name} chose Healer! (+2 ATK, +3 DEF, +15 HP)")

    def heal(self, target: "Player"):
        heal_amount = 20
        target.hp = min(target.max_hp, target.hp + heal_amount)
        print(f"Healer restores {heal_amount} HP to {target.name}.")