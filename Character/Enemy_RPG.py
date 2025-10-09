from Character.Character_RPG import *
from items import *
import random
from inventory import Inventory

class Enemy :
    def __init__(self, name, hp, attack, defense, exp_reward):
        self.name = name
        self.hp = hp
        self.attack_power = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.defeated = 0
    
    def scale_difficulty(self):
        factor = 1 + (0.2 * self.defeated)
        scaled_hp = int(self.hp * factor)
        scaled_attack = int(self.attack * factor)
        scaled_defense = int(self.defense * factor)
        return {"hp": scaled_hp, "attack": scaled_attack, "defense": scaled_defense}
    
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack(self, target):
        damage = max(0, self.attack_power - target.defense)
        target.take_damage(damage)
        print(f"{self.name} attack {target.name} and deals {damage} damage!")
    
    def mark_defeated(self,player):
        self.defeated += 1
        player.exp += self.exp_reward
        print(f"{self.name} has killed you ({self.defeated}) next time, get stronger!")

    def loot_drop(self):
        pass

class goblin(Enemy):
    def __init__(self):
        super().__init__("Goblin",45,10,2,6)

    def attack(self, target):
        super().attack(target)


class spider(Enemy):
    def __init__(self):
        super().__init__("Spider",15,5,1,2)    
    def attack(self, target):
        super().attack(target)


class skeleton (Enemy):
    def __init__(self):
        super().__init__("Skeleton",30,10,2,7)    
    def attack(self, target):
        super().attack(target)


class zombie(Enemy):
    def __init__(self):
        super().__init__("Zombie",35,10,2,6)
    def attack(self, target):
        super().attack(target)

# Boss Dungeon
class Wolf(Enemy):
    def __init__(self):
        super().__init__("Wolf",75,20,5,25)

    def attack(self, target):
        super().attack(target)
        target.status_effect.append("bleeding")
        print(f"{target.name} bleeding!")

class Ogre(Enemy):
    def __init__(self):
        super().__init__("Ogre",80,15,5,30)

    def attack(self, target):
        super().attack(target)
        target.status_effect.append("weakened")
        print(f"{target.name} stats temporarily down (weakened)!")

class Vampire(Enemy):
    def __init__(self):
        super().__init__("Vampire",65,30,5,35)

    def attack(self, target):
        super().attack(target)
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name}suck blood! HP recovers {heal}.")

# Last Boss
class Demon(Enemy):
    def __init__(self):
        super().__init__("Demon",hp=60, attack=30, defense= 3, exp_reward= 25)
        
    def attack(self, target):
        super().attack(target)
        target.status_effect.append("bleeding_demon")
        print(f"{target.name}  bleeding!")
        target.status_effect.append("weakened_demon")
        print(f"{target.name} stats temporarily down (weakened)!")
        heal = int(self.attack_power * 0.5)
        self.hp += heal
        print(f"{self.enemy_name} drains life and restores {heal} HP!")
