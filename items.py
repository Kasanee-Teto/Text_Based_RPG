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

Fists = Weapon("Fists","Unarmed",2,0)

class Armor(Items):
    def __init__(self, name , defense , defense_type , value  ):
        super().__init__(name,value)

        self.defense = defense
        self.defense_type = defense_type

Wizards_Robe = Armor ("Wizard's robe" , 2 , "Magic" , 10 )
Leather_Armor = Armor ("Leather Armor", 3 , "sharp" , 5)

# class Consumables(Items):
#     def __init__(self, name, value , amount_of_uses ):
#         super().__init__(name, value)
#         self.amount_of_uses=amount_of_uses

class Health_Potions(Items):
    def __init__(self, name, value , heals ):
        super().__init__(name, value)
        self.heals = heals

    def uses( self , entity ):
        entity.hp += self.heals
        print (f"{entity.name} drank {self.name} and healed {self.heals} HP")
    
Small_HPotion = Health_Potions("Small Health Potion",10,25)
Medium_HPotion = Health_Potions("Medium Health Potion",20,35)
Large_HPotion = Health_Potions("Medium Health Potion",30,50)
XL_HPotion = Health_Potions("The dev is too lazy to make potion names",40,80)



