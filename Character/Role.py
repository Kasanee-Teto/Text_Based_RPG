class Role:
    def __init__(self, name, bonus_attack=0, bonus_defense=0, bonus_hp=0):
        self.name = name
        self.bonus_attack = bonus_attack
        self.bonus_defense = bonus_defense
        self.bonus_hp = bonus_hp

    def apply_bonus(self, player):
        player.attack_power += self.bonus_attack
        player.defense += self.bonus_defense
        player.hp += self.bonus_hp
        print(f"{player.name} memilih role {self.name}! (Bonus: +{self.bonus_attack} ATK, +{self.bonus_defense} DEF, +{self.bonus_hp} HP)")

class Warrior(Role):
    def __init__(self):
        super().__init__("Warrior", bonus_attack=3, bonus_defense=5, bonus_hp=30)

class Mage(Role):
    def __init__(self):
        super().__init__("Mage", bonus_attack=10, bonus_defense=-2, bonus_hp=0)

class Archer(Role):
    def __init__(self):
        super().__init__("Archer", bonus_attack=7, bonus_defense=2, bonus_hp=10)

class Healer(Role):
    def __init__(self):
        super().__init__("Healer", bonus_attack=2, bonus_defense=3, bonus_hp=15)

    def heal(self, target):
        heal_amount = 20
        target.hp += heal_amount
        print(f"{self.name} menggunakan Heal! {target.name} bertambah {heal_amount} HP.")
