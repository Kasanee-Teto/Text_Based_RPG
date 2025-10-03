from Character_RPG import character


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
