class Enemy_RPG :
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