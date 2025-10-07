from Character.Character_RPG import *
from Character.Enemy_RPG import *
from items import *
from Character.Role import *
from save_game_RPG import *
import random

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
        else:
            print(f"\nWelcome, {player.name}!\n")
            
            # Musuh biasa
            enemy_list=[goblin(),spider(),skeleton(),zombie()]
            # Pilih musuh secara acak
            random_enemy = random.choice(enemy_list)

            print(f"\n{player.name} VS {random_enemy.name}")
            print("=========================")

            #Pertarungan
            while player.is_alive() and random_enemy.is_alive():

                #Giliran player
                pilihan = input("\nEnter = untuk menyerang\nE = untuk menggunakan item")
                if pilihan.lower() == 'e':
                    if player.inventory:
                        print("Choose an item to equip/use:")
                        for idx, item in enumerate(player.inventory, start=1):
                            print(f"{idx}. {item.name} (Value: {item.value})")
                        try:
                            item_choice = int(input("Enter the item number (or 0 to cancel): "))
                            if item_choice == 0:
                                continue
                            selected_item = player.inventory[item_choice - 1]
                            if selected_item in [Small_HPotion, Medium_HPotion]:
                                selected_item.uses()
                                print(f"You Use {selected_item.name} to heal.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip weapon
                            elif isinstance(selected_item, Weapon):
                                player.equipped_weapon = selected_item
                                print(f"You equipped {selected_item.name} as your weapon.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip armor
                            elif isinstance(selected_item, Armor):
                                player.equipped_armor = selected_item
                                print(f"You equipped {selected_item.name} as your armor.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            else:
                                print("You can only use potions, weapons, or armor.")
                        except (ValueError, IndexError):
                            print("Invalid choice!")
                    else:
                        print("Your inventory is empty.")
                else:
                    player.attack(random_enemy)
                print("=========================")
                # Giliran Musuh
                random_enemy.attack(player)
                print(f"{player.name} : {player.hp}")                
                print(f"{random_enemy.name} : {random_enemy.hp}")
                print("=========================")

               # Musuh mati
                if not random_enemy.is_alive():
                    print(f"{random_enemy.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {random_enemy.exp_reward} EXP\n")
                
                # Item 
                possible_drops = [Short_Sword, Short_bow, Fists, Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
                if random.random() < 0.5:  #50% untuk mendapatkan item
                    dropped_item = random.choice(possible_drops)
                    player.inventory.append(dropped_item)
                    print(f"{random_enemy.name} dropped a {dropped_item.name}! It has been added to your inventory.")

                # player mati
                if not player.is_alive():
                    random_enemy.mark_defeated()
                    player.hp = player.max_hp #player hp kembali pulih ke hp awal
                    break
            #Boss
            boss_list=[Wolf(),Ogre(),Vampire()]
            random_boss = random.choice(boss_list)
            print("===========================")
            print("       [Boss Fight]      ")
            print(f"\n         {player.name} VS {random_boss.name}")
            print("===========================")
            
            #Pertarungan boss
            while player.is_alive() and random_boss.is_alive():

                #Giliran player
                pilihan = input("\nEnter = untuk menyerang\nE = untuk menggunakan item")
                if pilihan.lower() == 'e':
                    if player.inventory:
                        print("Choose an item to equip/use:")
                        for idx, item in enumerate(player.inventory, start=1):
                            print(f"{idx}. {item.name} (Value: {item.value})")
                        try:
                            item_choice = int(input("Enter the item number (or 0 to cancel): "))
                            if item_choice == 0:
                                continue
                            selected_item = player.inventory[item_choice - 1]
                            if selected_item in [Small_HPotion, Medium_HPotion]:
                                selected_item.uses()
                                print(f"You Use {selected_item.name} to heal.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip weapon
                            elif isinstance(selected_item, Weapon):
                                player.equipped_weapon = selected_item
                                print(f"You equipped {selected_item.name} as your weapon.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip armor
                            elif isinstance(selected_item, Armor):
                                player.equipped_armor = selected_item
                                print(f"You equipped {selected_item.name} as your armor.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            else:
                                print("You can only use potions, weapons, or armor.")
                        except (ValueError, IndexError):
                            print("Invalid choice!")
                    else:
                        print("Your inventory is empty.")
                else:
                    player.attack(random_boss)
                print("=========================")
                # Hp Boss
                print(f"{random_boss.name} : {random_boss.hp}")
                print(f"{player.name} : {player.hp}\n")
                print("=========================")
                
                # player mati
                if not player.is_alive():
                    random_enemy.mark_defeated()
                    player.hp = player.max_hp #player hp kembali pulih ke hp awal
                    break
                
                # Boss mati
                if not random_boss.is_alive():
                    print(f"{random_boss.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {random_boss.exp_reward} exp\n")
                    
                    #Item Drop untuk Boss
                    possible_drops = [Short_Sword, Short_bow, Fists, Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
                    if random.random() < 0.8:  # 80% chance to drop (bosses drop more often)
                        dropped_item = random.choice(possible_drops)
                        player.inventory.append(dropped_item)
                        print(f"{random_boss.name} dropped a {dropped_item.name}! It has been added to your inventory.")
                    break
            #Last Boss
            print("===========================")
            print("       [Boss Fight]      ")
            print(f"\n         {player.name} VS {Demon.name}")
            print("===========================")
            while player.is_alive() and Demon.is_alive():
                #Giliran player
                pilihan = input("\nEnter = untuk menyerang\nE = untuk menggunakan item")
                if pilihan.lower() == 'e':
                    if player.inventory:
                        print("Choose an item to equip/use:")
                        for idx, item in enumerate(player.inventory, start=1):
                            print(f"{idx}. {item.name} (Value: {item.value})")
                        try:
                            item_choice = int(input("Enter the item number (or 0 to cancel): "))
                            if item_choice == 0:
                                continue
                            selected_item = player.inventory[item_choice - 1]
                            if selected_item in [Small_HPotion, Medium_HPotion]:
                                selected_item.uses()
                                print(f"You Use {selected_item.name} to heal.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip weapon
                            elif isinstance(selected_item, Weapon):
                                player.equipped_weapon = selected_item
                                print(f"You equipped {selected_item.name} as your weapon.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            # Equip armor
                            elif isinstance(selected_item, Armor):
                                player.equipped_armor = selected_item
                                print(f"You equipped {selected_item.name} as your armor.")
                                player.inventory.remove(selected_item)
                                print("===================================================")
                            else:
                                print("You can only use potions, weapons, or armor.")
                        except (ValueError, IndexError):
                            print("Invalid choice!")
                    else:
                        print("Your inventory is empty.")
                else:
                    player.attack(Demon)
                print("=========================")
                # Hp Boss
                print(f"{Demon.name} : {Demon.hp}")
                print(f"{player.name} : {player.hp}\n")
                print("=========================")
                
                # player mati
                if not player.is_alive():
                    Demon.mark_defeated()
                    player.hp = player.max_hp #player hp kembali pulih ke hp awal
                    break
                
                # Boss mati
                if not Demon.is_alive():
                    print(f"{Demon.name} Lose! {player.name} Win!")
                    print(f"{player.name} got : {Demon.exp_reward} exp\n")
                    
                    #Item Drop untuk Boss
                    possible_drops = [Short_Sword, Short_bow, Fists, Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
                    if random.random() < 0.8:  # 80% chance to drop (bosses drop more often)
                        dropped_item = random.choice(possible_drops)
                        player.inventory.append(dropped_item)
                        print(f"{Demon.name} dropped a {dropped_item.name}! It has been added to your inventory.")
                    break

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
        print("Exiting game...\n")
        break

print("========================================================")
print("|Thank you for playing the game                        |")
print("|Dibuat Oleh : Edbert Chandra, Kindy Lim, Louis Fortino|")
print("========================================================")

