from Character_RPG import Player
from Enemy_RPG import Goblin, spider, skeleton, zombie, Wolf, Ogre, Vampire, Demon
from items import Weapon, Armor, Health_Potions
from Role import Warrior, Archer, Mage, Healer
from save_game_RPG import save_games, load_game

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

    if choice == 1:
        if player is None:
            name = input("Enter your name (or 'back' to return): ")
            if name.lower() == "back":
                continue
            else:
                player = Player(name)
                print(f"Player {player.name} has been created!")
        else :
            print("Game already Started!")
            print()

    elif choice == 2:
        if player is not None :
            print(f"\nName: {player.name}")
            print(f"HP: {player.hp}")
            print(f"ATK: {player.attack_power}")
            print(f"DEF: {player.defense}")
            print(f"Level: {player.level}")
            print(f"Role: {player.role.name if player.role else 'None'}")
        else :
            print("Don't have an account yet, please create an account first")
        
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
            else :
                print("You cannot choose a role yet.")
        else:
            print("Start the game first!")
    
    elif choice == 4:
        if player:
            save_games(player)
        else:
            print("No player to save!")

    elif choice == 5:
        player = load_game()

    elif choice == 6:
        print("Exiting game...")
        break