from Character.Character_RPG import *
from Character.Enemy_RPG import *
from items import *
from Character.Role import *
from save_game_RPG import *
import random

player_inventory = Inventory()
player = None

def battle(player, enemy):
    print(f"\n{player.name} VS {enemy.name}")
    print("=========================")
    while player.is_alive() and enemy.is_alive():
        #Giliran player
        pilihan = input("\nEnter = untuk menyerang\nE = untuk menggunakan item")
        if pilihan.lower() == 'e':
            if player_inventory:
                print("Choose an item to equip/use:")
                player_inventory.list_items()
                try:
                    item_choice = int(input("Enter the item number (or 0 to cancel): "))
                    if item_choice == 0:
                        continue
                    selected_item = player.inventory[item_choice - 1]
                    if selected_item in Health_Potions:
                        selected_item.uses()
                        player_inventory.use_consumeable(selected_item)
                        print("===================================================")
                    elif selected_item in Weapon:
                        player.equip_weapon(selected_item)
                        print("===================================================")
                    elif selected_item in Armor:
                        player.equip_armor(selected_item)
                        print("===================================================")
                    else:
                        print("You can only use potions, weapons, or armor.")
                except (ValueError, IndexError):
                    print("Invalid choice!")
            else:
                print("Your inventory is empty.")
        else:
            player.attack(enemy)

        print("=========================")

        if enemy.is_alive():
            enemy.attack(player)
        print(f"{player.name} : {player.hp}")                
        print(f"{enemy.name} : {enemy.hp}")
        print("=========================")

def drop_item(player, enemy, drop_chance=0.5):
    possible_drops = [Short_Sword, Short_bow, Fists, Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
    if random.random() < drop_chance:
        dropped_item = random.choice(possible_drops)
        player.inventory.append(dropped_item)
        print(f"{enemy.name} dropped a {dropped_item.name}! It has been added to your inventory.")

def game_loop():
    global player
    while True:
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
            else:
                print(f"\nWelcome, {player.name}!\n")
                # Normal enemy
                enemy_list = [goblin(), spider(), skeleton(), zombie()]
                random_enemy = random.choice(enemy_list)
                battle(player, random_enemy)
                if not random_enemy.is_alive():
                    print(f"{random_enemy.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {random_enemy.exp_reward} EXP\n")
                    drop_item(player, random_enemy, 0.5)
                if not player.is_alive():
                    random_enemy.mark_defeated()
                    player.hp = player.max_hp
                    continue

                # Boss
                boss_list = [Wolf(), Ogre(), Vampire()]
                random_boss = random.choice(boss_list)
                print("===========================")
                print("       [Boss Fight]      ")
                battle(player, random_boss)
                if not player.is_alive():
                    random_boss.mark_defeated()
                    player.hp = player.max_hp
                    continue
                if not random_boss.is_alive():
                    print(f"{random_boss.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {random_boss.exp_reward} exp\n")
                    drop_item(player, random_boss, 0.8)

                # Last Boss
                DemonBoss = Demon()
                print("===========================")
                print("       [Final Boss Fight]      ")
                battle(player, DemonBoss)
                if not player.is_alive():
                    DemonBoss.mark_defeated()
                    player.hp = player.max_hp
                    continue
                if not DemonBoss.is_alive():
                    print(f"{DemonBoss.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {DemonBoss.exp_reward} exp\n")
                    drop_item(player, DemonBoss, 0.8)

        elif choice == 2:
            if player is not None:
                print(f"\nName: {player.name}")
                print(f"HP: {player.hp}")
                print(f"ATK: {player.attack_power}")
                print(f"DEF: {player.defense}")
                print(f"Level: {player.level}")
                print(f"Role: {player.role.name if player.role else 'None'}")
            else:
                print("Don't have an account yet, please create an account first")

        elif choice == 3:
            if player:
                if player.level >= 5 and player.role is None:
                    print("Choose your Role: ")
                    print("1. Warrior")
                    print("2. Mage")
                    print("3. Archer")
                    print("4. Healer")
                    print("5. back")
                    try:
                        choice_role = int(input("select role number (go back if you don't want to choose) : "))
                    except ValueError:
                        print("Invalid Choice !")
                        continue
                    if choice_role == 1:
                        player.choose_role(Warrior)
                    elif choice_role == 2:
                        player.choose_role(Mage)
                    elif choice_role == 3:
                        player.choose_role(Archer)
                    elif choice_role == 4:
                        player.choose_role(Healer)
                    elif choice_role == 5:
                        continue
                    else:
                        print("Invalid role Choice")
                else:
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
            print("Exiting game...\n")
            break

    print("========================================================")
    print("|Thank you for playing the game                        |")
    print("|Dibuat Oleh : Edbert Chandra, Kindy Lim, Louis Fortino|")
    print("========================================================")

if __name__ == "__main__":
    game_loop()