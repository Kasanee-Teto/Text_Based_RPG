from Character.Role import *
from inventory import Inventory
import math

class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp   #Simpan character hp
        self.attack_power = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
    
    def defeated(self,entity):
        pass

    def attack(self, target):
        damage = max(0, self.attack_power - target.defense)
        target.take_damage(damage)
        print(f"{self.name} attack {target.name} and deals {damage} damage!")


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=8, defense=2)
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.role = None
        self.status_effect = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.inventory = Inventory()
        self.coins = 200 # tambahkan coin player di sini

    def level_up(self):
        if self.exp >= self.exp_needed :
            self.level += 1
            self.hp += 20
            self.attack_power += 5
            self.defense += 2
            self.exp -= self.exp_needed
            self.exp_needed += self.level * math.sqrt(self.exp_needed)
            print(f"{self.name} level up! Now levels {self.level}.")
            if self.level == 5 and self.role is None :
                print(f"{self.name} can now choose a role (Warrior, Mage, Archer, Healer)!")

    def choose_role(self, role):
        if self.level >=5 and self.role is None:
            self.role = role
            role.apply_bonus(self)
        else :
            print("Can't select Role yet!")

    def equip_weapon(self,weapon):
        if weapon in self.inventory.items:
            if self.equipped_weapon == None :
                print (f"{self.name} equipped {weapon.name} ")
                self.inventory.remove_item(weapon)
                self.equipped_weapon = weapon
                self.attack_power+= self.equipped_weapon.damage

            else:
                print (f"{self.name} swapped {self.equipped_weapon.name} with {weapon.name}")
                self.attack_power -= self.equipped_weapon.damage
                self.inventory.add_item(self.equipped_weapon)
                self.inventory.remove_item(weapon)
                self.equipped_weapon = weapon
                self.attack_power+= self.equipped_weapon.damage

    def equip_armor(self,armor):
            if armor in self.inventory.items:
                if self.equipped_armor == None :   
                    print (f"{self.name} equipped {armor.name} ")
                    self.inventory.remove_item(armor)
                    self.equipped_armor = armor
                    self.defense += self.equipped_armor.defense

                else:
                    self.defense -= self.equipped_armor.defense 
                    print (f"{self.name} swapped {self.equipped_armor.name} with {armor.name}")
                    self.inventory.add_item(self.equipped_armor)
                    self.inventory.remove_item(armor)
                    self.equipped_armor = armor
                    self.defense += self.equipped_armor.defense

    def defeated(self, enemy):
        print (f"{enemy.name} has killed {self.name} ! \n Come back when you are stronger !\n" )
        
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

    def buy_item(self, shop, item_name):
        for item in shop.inventory_shop:
            if item["name"].lower() == item_name.lower():
                if self.coins >= item["price"]:
                    self.coins -= item["price"]
                    self.inventory.append(item)
                    print(f"{self.name} bought {item['name']} for {item['price']} coins.")
                else:
                    print("Not enough coins!")
                return
        print("Item not found in shop.")
    
    # JUAL ITEM
    def sell_item(self, item_name):
        for item in self.inventory:
            if item["name"].lower() == item_name.lower():
                sell_price = int(item["price"] * 0.5)  # harga jual 50%
                self.inventory.remove(item)
                self.coins += sell_price
                print(f"{self.name} sold {item['name']} for {sell_price} coins.")
                return
        print(f"{item_name} not found in inventory.")

    # TERIMA ITEM (misal drop musuh)
    def receive_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} received {item['name']}!")
