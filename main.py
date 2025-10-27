from Character.Character_RPG import Player
from Character.Enemy_RPG import *
from items import Items, Weapon, Armor, Health_Potions
from Character.Role import Warrior, Mage, Archer, Healer
from save_game_RPG import save_games, load_game
from Shop import shop_sword, shop_armor, shop_potion 

from colorama import Fore, Style, init
init(autoreset=True)

import random

player = None

def inventory_menu():
    running = True 

    if player == None :
        print ("Buat Karakter Terlebih Dahulu !")
        running = False
    
    while running :
        print ("Inventory Menu")
        print ("1.Show Inventory ")
        print ("2.Drop Item")
        print ("3.Equip/Use Item")
        print ("4.Show Item Description")
        print ("5.Close Menu")
        try :
            inv_choice = int (input ("Choose Action = "))
            if inv_choice == 1 :
                player.inventory.list_items()
            elif inv_choice == 2 :
                idx = int(input("Choose item's index to remove = "))
                selected_item = player.inventory.items[idx-1]
                player.inventory.remove_item((selected_item))
            elif inv_choice == 3 :
                if player.inventory:
                    print("Choose an item to equip/use:")
                    player.inventory.list_items()
                    try:
                        item_choice = int(input("Enter the item number (or 0 to cancel): "))
                        if item_choice == 0:
                            continue
                        selected_item = player.inventory.items[item_choice-1]
                        if isinstance(selected_item, Health_Potions):
                            player.inventory.use_consumeable(selected_item,player)
                            print("===================================================")
                        elif isinstance(selected_item, Weapon):
                            player.equip_weapon(selected_item)
                            print("===================================================")
                        elif isinstance(selected_item, Armor):
                            player.equip_armor(selected_item)
                            print("===================================================")
                        else:
                            print("You can only use potions, weapons, or armor.")
                    except (ValueError, IndexError):
                        print("Invalid choice!")
                else:
                    print("Your inventory is empty.")
                    print("=========================")
            elif inv_choice == 4 :
                idx = int(input("Enter item's index ="))
                selected_item = player.inventory.items[idx-1]
                selected_item.desc()
            elif inv_choice == 5 :
                running = False
                print ("=========================")

        except(ValueError,IndexError):
            print("Invalid choice!")

def battle(player, enemy):
    print(f"\n{player.name} VS {enemy.name}")
    print("=========================")
    while player.is_alive() and enemy.is_alive():
        #Giliran player
        pilihan = input("\nEnter = Attack \nE = Open Inventory \n")
        if pilihan.lower() == 'e':
            inventory_menu()
        else :
            player.attack(enemy)
            print("=========================")

        if enemy.is_alive():
            enemy.attack(player)
            print(f"{player.name} : {player.hp}")                
            print(f"{enemy.name} : {enemy.hp}")
            print("=========================") 

    player.level_up()

def drop_item(player, enemy, drop_chance=0.5):
    possible_drops = [Short_Sword, Short_bow,Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
    if random.random() < drop_chance:
        dropped_item = random.choice(possible_drops)
        player.inventory.add_item(dropped_item)
        print(f"{enemy.name} dropped a {dropped_item.name}! It has been added to your inventory.")

def game_loop():
    global player
    while True:
        print(Fore.YELLOW + Style.BRIGHT + "="*50)
        print(Fore.CYAN + Style.BRIGHT + "      ⚔️  WELCOME TO THE RPG ADVENTURE  ⚔️")
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + "1. Start Game")
        print("2. Show Status")
        print("3. Choose Role")
        print("4. Shop 🛒")
        print("5. Inventory 🎒")
        print("6. Save Game 💾")
        print("7. Load Game 📂")
        print("8. Exit ❌")
        print(Fore.YELLOW + "="*50)
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
                    random_enemy.defeated(player)
                    drop_item(player, random_enemy, 0.5)

                if not player.is_alive():
                    player.defeated(random_enemy)
                    player.hp = player.max_hp
                    player.status_effect = []
                    continue

                # Boss
                boss_list = [Wolf(), Ogre(), Vampire()]
                random_boss = random.choice(boss_list)
                print("===========================")
                print("       [Boss Fight]      ")
                battle(player, random_boss)
                if not player.is_alive():
                    player.defeated(random_boss)
                    player.hp = player.max_hp
                    player.status_effect = []
                    continue

                if not random_boss.is_alive():
                    random_boss.defeated(player)
                    print(f"{random_boss.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {random_boss.exp_reward} exp\n")
                    drop_item(player, random_boss, 0.8)

                # Last Boss
                Demon_Boss = Demon()
                print("===========================")
                print("       [Final Boss Fight]      ")
                battle(player, Demon_Boss)
                if not player.is_alive():
                    player.defeated(Demon_Boss)
                    player.hp = player.max_hp
                    player.status_effect = []
                    continue

                if not Demon_Boss.is_alive():
                    Demon_Boss.defeated(player)
                    print(f"{Demon_Boss.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {Demon_Boss.exp_reward} exp\n")
                    drop_item(player, Demon_Boss, 0.7)

        elif choice == 2:
            if player is not None:
                print(f"\nName: {player.name}")
                print(f"HP: {player.hp}")
                print(f"ATK: {player.attack_power}")
                print(f"DEF: {player.defense}")
                if player.equipped_weapon is not None :
                    print(f"Weapon: {player.equipped_weapon.name}")
                else :
                    print("Weapon: Unarmed")
                if player.equipped_armor is not None :
                    print(f"Armor: {player.equipped_armor.name}")
                else :
                    print("Armor: Unarmored")
                print(f"Level: {player.level}")
                print(f"Exp: {player.exp} / {player.exp_needed}")
                print(f"Role: {player.role.name if player.role else 'None'}")
                print(f"Status Effect : {player.status_effect}")

            else:
                print("Don't have an character yet, please create a character first")

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
                while True:
                    print("\n🛒 === Welcome to the Shop ===")
                    print("1. Sword Shop")
                    print("2. Armor Shop")
                    print("3. ")
                    print("3. Potion Shop")
                    print("4. Back")
                    print(f"💰 Your Coins: {player.coins}")
                    try:
                        shop_choice = int(input("Choose shop category: "))
                    except ValueError:
                        print("Invalid input!")
                        continue

                    # ====== SHOP SECTION ======
                    if shop_choice == 1:
                        weapon_shop = shop_sword()
                        weapon_shop.stock_sword_dagger()
                        weapon_shop.stock_sword_katana()
                        weapon_shop.stock_sword_great_sword()

                        weapon_shop.show_items("⚔️ Available Swords")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = weapon_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.append(selected)
                                selected["stock"] -= 1
                                print(f"\n✅ You bought {selected['name']}! It's added to your inventory.")
                            else:
                                print("❌ Not enough coins!")
                        except (ValueError, IndexError):
                            print("Invalid choice!")

                    elif shop_choice == 2:
                        armor_shop = shop_armor()
                        armor_shop.stock_light_armor()
                        armor_shop.stock_heavy_armor()
                        armor_shop.stock_medium_armor()

                        armor_shop.show_items("🛡️ Available Armors")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = armor_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.append(selected)
                                selected["stock"] -= 1
                                print(f"\n✅ You bought {selected['name']}! It's added to your inventory.")
                            else:
                                print("❌ Not enough coins!")
                        except (ValueError, IndexError):
                            print("Invalid choice!")

                    elif shop_choice == 3:
                        potion_shop = shop_potion()
                        potion_shop.stock_health_potions()

                        potion_shop.show_items("🧪 Available Potions")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = potion_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.append(selected)
                                selected["stock"] -= 1
                                print(f"\n✅ You bought {selected['name']}! It's added to your inventory.")
                            else:
                                print("❌ Not enough coins!")
                        except (ValueError, IndexError):
                            print("Invalid choice!")
                        
                    elif shop_choice == 4:
                        print("Exiting shop...")
                        break
            else:
                print("⚠️ Start the game first before visiting the shop!")

        elif choice == 5:
            inventory_menu()

        elif choice == 6:
            if player:
                save_games(player)
            else:
                print("No player to save!")

        elif choice == 7:
            player = load_game()

        elif choice == 8:
            print("Exiting game...\n")
            break

    print("========================================================")
    print("|Thank you for playing the game                        |")
    print("|Dibuat Oleh : Edbert Chandra, Kindy Lim, Louis Fortino|")
    print("========================================================")

if __name__ == "__main__":
    game_loop()