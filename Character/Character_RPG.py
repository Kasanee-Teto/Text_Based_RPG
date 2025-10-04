from .Role import Role
from items import Leather_armor,Fists
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
        print(f"{self.name} attack {target.name} and deals {damage} damage!")
        
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
        print(f"{self.name} level up! Now levels {self.level}.")
        if self.level == 5 and self.role is None :
            print(f"{self.name} can now choose a role (Warrior, Mage, Archer, Healer)!")

    def choose_role(self, role):
        if self.level >=5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
        else :
            print("Can't select Role yet!")

    def status_effect(self):
        if "bleeding" in self.status_effect:
            bleed_damage = 3
            self.hp -= bleed_damage
            print(f"{self.name} uffers from bleeding and loses {bleed_damage} HP.")

        elif "bleeding_demon" in self.status_effect:
            bleed_damage_demon = 5
            self.hp -= bleed_damage_demon
            print(f"{self.name} uffers from bleeding and loses {bleed_damage_demon} HP.")

        if "weakened" in self.status_effects:
            weakened_atk = max(1, int(self.attack_power * 0.8))
            weakened_def = max(1, int(self.defense * 0.8))
            print(f"{self.name} is weakened! ATK {self.attack_power}->{weakened_atk}, DEF {self.defense}->{weakened_def}")
            self.attack_power = weakened_atk
            self.defense = weakened_def

        elif "weakened_demon" in self.status_effect:
            weakened_atk_demon = max(1, int(self.attack_power * 0.6))
            weakened_def_demon = max(1, int(self.defense * 0.6))
            print(f"{self.name} is weakened! ATK {self.attack_power}->{weakened_atk_demon}, DEF {self.defense}->{weakened_def_demon}")
            self.attack_power = weakened_atk_demon
            self.defense = weakened_atk_demon



