from Role import Role
class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack_power = attack
        self.defense = defense

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


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=15, defense=5)
        self.exp = 0
        self.level = 1
        self.role = None

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.attack_power += 5
        self.defense += 2
        print(f"{self.name} naik level! Sekarang level {self.level}.")
        if self.level == 5 and self.role is None :
            print(f"{self.name} sekarang bisa memilih role (Warrior, Mage, Archer, Healer)!")

    def choose_role(self, role):
        if self.level >=5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
        else :
            print("Belum bisa memilih Role!")