"""
Enemy module dengan SOLID:
- SRP: Enemy fokus pada perilaku musuh dan hadiah EXP.
- OCP: Tambah musuh baru cukup dengan subclass Enemy.
- LSP: Enemy tetap substitutable sebagai Character.
- DIP: Defeated memberi EXP via Player API (Player punya exp property).
"""

from Character.Character_RPG import Character, Player
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Character.Character_RPG import Player as PlayerType


class Enemy(Character):
    def __init__(self, name: str, hp: int, attack: int, defense: int, exp_reward: int):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward
        self.defeated_count = 0

    def scale_difficulty(self, factor: float = 1.0) -> dict:
        return {
            "hp": int(self.max_hp * factor),
            "attack": int(self.attack_power * factor),
            "defense": int(self.defense * factor),
        }

    def defeated(self, player: "PlayerType"):
        self.defeated_count += 1
        player.exp += self.exp_reward
        print(f"🏆 {self.name} defeated! {player.name} wins!")
        print(f"💫 {player.name} gained {self.exp_reward} EXP\n")


# Normal enemies (constants kept for backward compatibility)
def GoblinGrunt():
    return Enemy("Goblin Grunt", 45, 10, 2, 15)

def CaveSpider():
    return Enemy("Cave Spider", 20, 7, 1, 8)

def Skeleton():
    return Enemy("Skeleton", 30, 10, 2, 11)

def Zombie():
    return Enemy("Zombie", 35, 10, 2, 13)


class WolfBoss(Enemy):
    def __init__(self):
        super().__init__("Alpha Wolf", 75, 20, 5, 25)

    def attack(self, target: Player):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"🩸 {target.name} is bleeding!")


class OgreBoss(Enemy):
    def __init__(self):
        super().__init__("Ogre Brute", 80, 15, 5, 30)

    def attack(self, target: Player):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"💢 {target.name}'s stats are temporarily reduced (weakened)!")


class VampireBoss(Enemy):
    def __init__(self):
        super().__init__("Vampire Lord", 65, 30, 5, 35)

    def attack(self, target: Player):
        damage = super().attack(target)
        heal = int(damage * 0.3)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"🧛 {self.name} drains blood!  HP recovered {heal} (HP: {self.hp}/{self.max_hp})")


class DemonBoss(Enemy):
    def __init__(self):
        super().__init__("Demon King", 100, 30, 3, 50)

    def attack(self, target: Player):
        damage = super().attack(target)
        target.status_effects.append("bleeding_demon")
        print(f"🩸 {target.name} is severely bleeding!")
        target.status_effects.append("weakened_demon")
        print(f"💢 {target.name}'s stats are severely reduced!")
        heal = int(damage * 0.5)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"😈 {self.name} drains life force and restores {heal} HP!")