from .Character_RPG import Player
class Enemy(Character):
    def __init__(self, name, hp, attack, defense, exp_reward=0):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward
        self.defeated = 0
        self.status_effects = []

    def scale_difficulty(self):
        factor = 1 + (0.2 * self.defeated)
        scaled_hp = int(self.enemy_hp * factor)
        scaled_attack = int(self.enemy_attack * factor)
        scaled_defense = int(self.enemy_defense * factor)
        return {"hp": scaled_hp, "attack": scaled_attack, "defense": scaled_defense}

    def mark_defeated(self):
        self.defeated += 1
        print(f"{self.enemy_name} has been defeated {self.defeated} next time, get stronger!")

# --- SUBCLASS ENEMY SPESIAL ---
# Normal Enemy
class Goblin(Enemy):
    def __init__(self):
        super().__init__("Goblin", 100, 20, 2, 10)
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
        super().__init__("Ogre",hp=80, attack=15, defense= 10, exp_reward= 25)

    def attack(self, target):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"{target.name} stats temporarily down (weakened)!")

class Vampire(Enemy):
    def __init__(self):
        super().__init__("Vampire",hp=60, attack=30, defense= 3, exp_reward= 25)

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
        target.status_effects.append("bleeding_demon")
        print(f"{target.name}  bleeding!")
        target.status_effects.append("weakened_demon")
        print(f"{target.name} stats temporarily down (weakened)!")
        heal = int(self.attack_power * 0.5)
        self.enemy_hp += heal
        print(f"{self.enemy_name} drains life and restores {heal} HP!")



