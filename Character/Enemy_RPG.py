from Character_RPG import Player
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
    
    def mark_defeated(self):
        self.defeated += 1
        print(f"{self.name} has been defeated {self.defeated} next time, get stronger!")
    
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack(self, target):
        damage = max(0, self.attack_power - target.defense)
        target.take_damage(damage)
        print(f"{self.name} menyerang {target.name} dan menyebabkan {damage} damage!")

class goblin(Enemy):
    def attack(self, target):
        super().attack(target)


class spider(Enemy):
    def attack(self, target):
        super().attack(target)


class skeleton (Enemy):
    def attack(self, target):
        super().attack(target)


class zombie(Enemy):
    def attack(self, target):
        super().attack(target)

# Boss Dungeon
class Wolf(Enemy):
    def __init__(self):
        super().__init__("Wolf",enemy_hp=50, enemy_attack=20, enemy_defense= 5, exp_reward= 25)

    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"{target.name} bleeding!")

class Ogre(Enemy):
    def __init__(self):
        super().__init__("Ogre",enemy_hp=80, enemy_attack=15, enemy_defense= 10, exp_reward= 25)

    def attack(self, target):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"{target.name} stats temporarily down (weakened)!")

class Vampire(Enemy):
    def __init__(self):
        super().__init__("Vampire",enemy_hp=60, enemy_attack=30, enemy_defense= 3, exp_reward= 25)

    def attack(self, target):
        super().attack(target)
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name}suck blood! HP recovers {heal}.")

# Last Boss
class Demon(Enemy):
    def __init__(self):
        super().__init__("Demon",enemy_hp=60, enemy_attack=30, enemy_defense= 3, exp_reward= 25)
        
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding_demon")
        print(f"{target.name}  bleeding!")
        target.status_effects.append("weakened_demon")
        print(f"{target.name} stats temporarily down (weakened)!")
        heal = int(self.attack_power * 0.5)
        self.enemy_hp += heal
        print(f"{self.enemy_name} drains life and restores {heal} HP!")
