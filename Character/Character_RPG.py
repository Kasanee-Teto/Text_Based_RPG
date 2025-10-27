from inventory import Inventory
import math


class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp  # Track maximum HP
        self.attack_power = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= max(0, damage)
        if self.hp < 0:
            self.hp = 0

    def defeated(self, entity):
        pass

    def attack(self, target):
        damage = max(0, self.attack_power - getattr(target, "defense", 0))
        target.take_damage(damage)
        print(f"{self.name} attack {target.name} and deals {damage} damage!")
        return damage


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=8, defense=2)
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.role = None
        self.status_effects = []  # renamed from status_effect to avoid name clash with method
        self.equipped_weapon = None
        self.equipped_armor = None
        self.inventory = Inventory()
        self.coins = 200

    def level_up(self):
        leveled_up = False
        while self.exp >= self.exp_needed:
            self.level += 1
            self.max_hp += 20
            # Heal a bit on level-up but don't exceed max
            self.hp = min(self.max_hp, self.hp + 20)
            self.attack_power += 5
            self.defense += 2
            self.exp -= self.exp_needed
            self.exp_needed += int(self.level * math.sqrt(self.exp_needed))
            print(f"{self.name} level up! Now level {self.level}.")
            leveled_up = True

        if leveled_up and self.level >= 5 and self.role is None:
            print(f"{self.name} can now choose a role (Warrior, Mage, Archer, Healer)!")

    def choose_role(self, role):
        if self.level >= 5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
        else:
            print("Can't select Role yet!")

    def equip_weapon(self, weapon):
        if weapon in self.inventory.items:
            if self.equipped_weapon is None:
                print(f"{self.name} equipped {weapon.name}")
                self.inventory.remove_item(weapon)
                self.equipped_weapon = weapon
                self.attack_power += getattr(self.equipped_weapon, "damage", 0)
            else:
                print(f"{self.name} swapped {self.equipped_weapon.name} with {weapon.name}")
                self.attack_power -= getattr(self.equipped_weapon, "damage", 0)
                self.inventory.add_item(self.equipped_weapon)
                self.inventory.remove_item(weapon)
                self.equipped_weapon = weapon
                self.attack_power += getattr(self.equipped_weapon, "damage", 0)

    def equip_armor(self, armor):
        if armor in self.inventory.items:
            if self.equipped_armor is None:
                print(f"{self.name} equipped {armor.name}")
                self.inventory.remove_item(armor)
                self.equipped_armor = armor
                self.defense += getattr(self.equipped_armor, "defense", 0)
            else:
                print(f"{self.name} swapped {self.equipped_armor.name} with {armor.name}")
                self.defense -= getattr(self.equipped_armor, "defense", 0)
                self.inventory.add_item(self.equipped_armor)
                self.inventory.remove_item(armor)
                self.equipped_armor = armor
                self.defense += getattr(self.equipped_armor, "defense", 0)

    def defeated(self, enemy):
        print(f"{enemy.name} has killed {self.name}! Come back when you are stronger!")

    def update_status_effects(self):
        # Bleeding effects
        if "bleeding" in self.status_effects:
            bleed_damage = 3
            self.hp = max(0, self.hp - bleed_damage)
            print(f"{self.name} suffers from bleeding and loses {bleed_damage} HP.")
        elif "bleeding_demon" in self.status_effects:
            bleed_damage_demon = 5
            self.hp = max(0, self.hp - bleed_damage_demon)
            print(f"{self.name} suffers from bleeding and loses {bleed_damage_demon} HP.")

        # Weakened effects
        if "weakened" in self.status_effects:
            weakened_atk = max(1, int(self.attack_power * 0.8))
            weakened_def = max(1, int(self.defense * 0.8))
            print(
                f"{self.name} is weakened! ATK {self.attack_power}->{weakened_atk}, "
                f"DEF {self.defense}->{weakened_def}"
            )
            self.attack_power = weakened_atk
            self.defense = weakened_def
        elif "weakened_demon" in self.status_effects:
            weakened_atk_demon = max(1, int(self.attack_power * 0.6))
            weakened_def_demon = max(1, int(self.defense * 0.6))
            print(
                f"{self.name} is weakened! ATK {self.attack_power}->{weakened_atk_demon}, "
                f"DEF {self.defense}->{weakened_def_demon}"
            )
            self.attack_power = weakened_atk_demon
            self.defense = weakened_def_demon

    def buy_item(self, shop, item_name):
        for item in getattr(shop, "inventory_shop", []):
            name = item.get("name") if isinstance(item, dict) else getattr(item, "name", None)
            price = item.get("price") if isinstance(item, dict) else getattr(item, "price", None)
            if name and name.lower() == item_name.lower():
                if price is not None and self.coins >= price:
                    self.coins -= price
                    self.inventory.add_item(item)
                    print(f"{self.name} bought {name} for {price} coins.")
                else:
                    print("Not enough coins!")
                return
        print("Item not found in shop.")

    def sell_item(self, item_name):
        for item in list(self.inventory.items):
            name = item.get("name") if isinstance(item, dict) else getattr(item, "name", None)
            price = item.get("price") if isinstance(item, dict) else getattr(item, "price", None)
            if name and name.lower() == item_name.lower():
                sell_price = int(price * 0.5) if price is not None else 0
                self.inventory.remove_item(item)
                self.coins += sell_price
                print(f"{self.name} sold {name} for {sell_price} coins.")
                return
        print(f"{item_name} not found in inventory.")

    def receive_item(self, item):
        self.inventory.add_item(item)
        item_name = item.get("name") if isinstance(item, dict) else getattr(item, "name", "item")
        print(f"{self.name} received {item_name}!")