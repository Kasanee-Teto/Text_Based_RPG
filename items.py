from abc import *

class Items():
    def __init__(self,name,value):
        self.name = name   
        self.value = value

class Weapon(Items):
    def __init__(self , name , weapon_type , damage , value):
        super().__init__(name,value)
        self.weapon_type = weapon_type
        self.damage = damage
    
Short_Sword = Weapon("Short_sword","Sharp",5,10)
Short_bow = Weapon("Short_bow","Ranged",4,8)
Long_Sword = Weapon("Long_Sword","Sharp",12,35)
Mace = Weapon("Mace","Blunt",8,25)

class Armor(Items):
    def __init__(self, name , defense , defense_type , value  ):
        super().__init__(name,value)

        self.defense = defense
        self.defense_type = defense_type

Wizards_Robe = Armor ("Wizard's Robe" , 2 , "Magic" , 10 )
Leather_Armor = Armor ("Leather Armor", 3 , ["Sharp","Blunt"] , 5)
Iron_Armor = Armor("Iron Armor", 12 , ["Sharp","Blunt"] , 50)

class Consumables():
    @abstractmethod
    def uses(self):
        pass

class Health_Potions(Items,Consumables):
    def __init__(self, name, value , heals ):
        super().__init__(name, value)
        self.heals = heals

    def uses( self , entity ):
        entity.hp += self.heals
        print (f"{entity.name} drank {self.name} and healed {self.heals} HP")
    
Small_HPotion = Health_Potions("Small Health Potion",10,25)
Medium_HPotion = Health_Potions("Medium Health Potion",20,35)
Large_HPotion = Health_Potions("Medium Health Potion",30,50)
XL_HPotion = Health_Potions("The dev is too lazy to make potion name",40,80)

# class Mana_Potion(Items,Consumeables):
#     def __init__(self, name, value , recover):
#         super().__init__(name, value)
#         self.recover = recover
    
#     def uses( self , entity ):
#         entity.mana += self.recover
#         print (f"{entity.name} drank {self.name} and recovered {self.recover} mana")

# class Rock_Potion(Items,Consumables):
#     def __init__(self, name, value , defense_mod):
#         super().__init__(name, value)
#         self.defense_mod = defense_mod

#     def uses(self , entity ):
#         entity.defense += self.defense_mod
#         print (f"{entity.name} drank {self.name} and got {self.defense_mod} defense boost for 5 turns") 