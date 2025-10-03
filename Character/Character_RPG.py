from character.role import Role
from items.items import Fists, Leather_Armor

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

    def attacks(self, target):
        damage = max(0, self.attack_power - target.defense)
        target.take_damage(damage)
        print(f"{self.name} menyerang {target.name} dan menyebabkan {damage} damage!")

class Player(Character):
    def __init__(self, name, hp=100, attack=15, defense=10):
        super().__init__(name, hp, attack, defense)
        self.weapon = Fists
        self.armor = Leather_Armor
        self.defense = defense + self.armor.defense
        self.attack_power = attack + self.weapon.damage
        self.exp = 0
        self.level = 1
        self.role = None
        self.status_effects = []

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def equip_armor(self, armor):
        self.armor = armor

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.attack_power += 5
        self.defense += 2
        print(f"{self.name} naik level! Sekarang level {self.level}.")
        if self.level == 5 and self.role is None:
            print(f"{self.name} sekarang bisa memilih role (Warrior, Mage, Archer, Healer)!")

    def choose_role(self, role):
        if self.level >= 5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
        else:
            print("Belum bisa memilih Role!")
