from Character_RPG import character

class Enemy(Character):
    def __init__(self, name, hp, attack, defense, exp_reward):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward
        self.defeated = 0

    def scale_difficulty(self):
        factor = 1 + (0.2 * self.defeated)
        scaled_hp = int(self.hp * factor)
        scaled_attack = int(self.attack_power * factor)
        scaled_defense = int(self.defense * factor)
        return {"hp": scaled_hp, "attack": scaled_attack, "defense": scaled_defense}

    def mark_defeated(self):
        self.defeated += 1
        print(f"{self.name} telah dikalahkan {self.defeated} kali, jadi lebih kuat!")
        
# --- SUBCLASS ENEMY SPESIAL ---
class Goblin(Enemy):
    def attack(self, target):
        super().attack(target)

class Wolf(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"{target.name} terkena bleeding!")


class Ogre(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"{target.name} stat turun sementara (weakened)!")


class Vampire(Enemy):
    def attack(self, target):
        super().attack(target)
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name} menyedot darah! HP pulih {heal}.")


class Demon(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"{target.name} terkena bleeding!")
        target.status_effects.append("weakened")
        print(f"{target.name} stat turun sementara (weakened)!")
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name} menyedot d arah! HP pulih {heal}.")

