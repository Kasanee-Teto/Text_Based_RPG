from Character.Character_RPG import Player
from Character.Enemy_RPG import Goblin, Wolf, Ogre, Vampire, Demon
from Character.Role import Warrior,Mage,Archer,Healer
from items import Leather_Armor,Short_bow,Short_Sword
import random

def menu():
    print("=== MENU RPG SEDERHANA ===")
    print("1. Mulai Game")
    print("2. Keluar")
    pilihan = input("Pilih menu: ")
    return pilihan

def main():

    player = None

    while True :
        print("=== Welcome to the RPG Game ===")
        print("1. Start Game")
        print("2. Show Status")
        print("3. Choose Role")
        print("4. Save Game")
        print("5. Load Game")
        print("6. Exit")
        try:
            choice = int(input("Enter Your choice : "))
        except ValueError:
            print("Invalid Choice!")
            continue
        if choice == 1 :
            if player is None :
                name = input("Please Your Name : ")
                player = Player(name)
                print(f"The Player {player.name} has been created!")
                print()
                
                #Bikin Enemy biasa
                e1 = Goblin
                e2 = Ogre
                e3 = Wolf

                enemy_list=[e1, e2, e3]
                random_enemy = random.choice(enemy_list)
                print(f"\n{player.name} VS {random_enemy.name}")
                print("=========================")

                #Pertarungan
                while player.is_alive() and random_enemy.is_alive():
                    input("\nTekan ENTER untuk menyerang...")
                    player.attack(random_enemy)

                    #Hp Enemy
                    print(f"{random_enemy.name} : {random_enemy.hp}")
                    print()
                    if not random_enemy.is_alive():
                        print(f"{random_enemy.name} kalah! {player.name} menang!")
                        break

                # Giliran Musuh
                    random_enemy.attack(player)
                    if not player.is_alive():
                        print(f"{player.name} kalah! {random_enemy.name} menang!")
                        print()
                        break
            else :
                print("Game already Started!")
                print()
                
        elif choice == 2:
            print(f"\nName: {player.name}")
            print(f"HP: {player.hp}")
            print(f"ATK: {player.attack_power}")
            print(f"DEF: {player.defense}")
            print(f"Level: {player.level}")
            print(f"Role: {player.role.name if player.role else 'None'}")
        
        elif choice == 3 :
            if player :
                if player.level >= 5 and player.role is None :
                    print("Choose your Role: ")
                    print("1. Warrior")
                    print("2. Mage")
                    print("3. Archer")
                    print("4. Healer")
                    print("5. back")
                    try :
                        choice_role = int(input("select role number (go back if you don't want to choose) : "))
                    except ValueError :
                        print("Invalid Choice !")
                        continue
                    if choice_role == 1 :
                        player.choose_role(Warrior)
                    elif choice_role == 2 :
                        player.choose_role(Mage)
                    elif choice_role == 3 :
                        player.choose_role(Archer)
                    elif choice_role == 4 :
                        player.choose_role(Healer)
                    elif choice_role == 5 :
                        continue
                    else :
                        print("Invalid role Choice")
        elif choice == 6 :
            break

print("Thank you for playing")
print("Dibuat oleh : Edbert Chandra, Kindy Lim, Louise Fortino")
if __name__ == "__main__":
    main()
