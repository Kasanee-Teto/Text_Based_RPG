from Character.Character_RPG import Player
from Character.Enemy_RPG import *
from items import *
from Character.Role import Warrior, Mage, Archer, Healer
from save_game_RPG import save_games, load_game
from Shop import shop_bow, shop_sword, shop_armor, shop_potion, shop_grimoire, shop_staff

from colorama import Fore, Style, init
init(autoreset=True)

import random

player = None

def inventory_menu():
    running = True 

    if player == None :
        print(Fore.RED + "⚠️  Create a character first!" + Style.RESET_ALL)
        running = False
    
    while running :
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "🎒 INVENTORY MENU".center(50) + Style.RESET_ALL)
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print("1) Show Inventory")
        print("2) Drop Item")
        print("3) Equip / Use Item")
        print("4) Show Item Description")
        print("5) Close Menu")
        print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
        try :
            inv_choice = int (input(Fore.CYAN + "Choose Action: " + Style.RESET_ALL))
            if inv_choice == 1 :
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                player.inventory.list_items()
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            elif inv_choice == 2 :
                idx = int(input("Choose item's index to remove: "))
                selected_item = player.inventory.items[idx-1]
                player.inventory.remove_item((selected_item))
                print(Fore.GREEN + "✅ Item removed." + Style.RESET_ALL)
            elif inv_choice == 3 :
                if player.inventory:
                    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                    print("Choose an item to equip/use:")
                    player.inventory.list_items()
                    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                    try:
                        item_choice = int(input("Enter the item number (or 0 to cancel): "))
                        if item_choice == 0:
                            continue
                        selected_item = player.inventory.items[item_choice-1]
                        if isinstance(selected_item, Health_Potions):
                            player.inventory.use_consumeable(selected_item,player)
                            print(Fore.GREEN + "🧪 Potion used!" + Style.RESET_ALL)
                            print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                        elif isinstance(selected_item, Weapon):
                            player.equip_weapon(selected_item)
                            print(Fore.GREEN + "⚔️  Weapon equipped!" + Style.RESET_ALL)
                            print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                        elif isinstance(selected_item, Armor):
                            player.equip_armor(selected_item)
                            print(Fore.GREEN + "🛡️  Armor equipped!" + Style.RESET_ALL)
                            print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                        else:
                            print(Fore.RED + "You can only use potions, weapons, or armor." + Style.RESET_ALL)
                    except (ValueError, IndexError):
                        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Your inventory is empty." + Style.RESET_ALL)
                    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            elif inv_choice == 4 :
                idx = int(input("Enter item's index: "))
                selected_item = player.inventory.items[idx-1]
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                selected_item.desc()
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            elif inv_choice == 5 :
                running = False
                print(Fore.YELLOW + "Closing Inventory..." + Style.RESET_ALL)
                print(Fore.YELLOW + "="*50 + Style.RESET_ALL)

        except(ValueError,IndexError):
            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

def battle(player, enemy):
    print(Fore.YELLOW + "\n" + "="*50 + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + f"{player.name}  VS  {enemy.name}".center(50) + Style.RESET_ALL)
    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
    while player.is_alive() and enemy.is_alive():
        # Player's turn
        pilihan = input(Fore.CYAN + "\nPress Enter to Attack, or 'E' to open Inventory: " + Style.RESET_ALL)
        if pilihan.lower() == 'e':
            inventory_menu()
        else :
            player.attack(enemy)
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)

        if enemy.is_alive():
            enemy.attack(player)
            print(Fore.GREEN + f"💚 {player.name} HP: {player.hp}" + Style.RESET_ALL)                
            print(Fore.RED + f"💔 {enemy.name} HP: {enemy.hp}" + Style.RESET_ALL)
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)

    player.level_up()

def drop_item(player, enemy, drop_chance=0.5):
    possible_drops = [Short_Sword, Short_bow, Long_Sword, Mace, Wizards_Robe, Leather_Armor, Small_HPotion, Medium_HPotion]
    if random.random() < drop_chance:
        dropped_item = random.choice(possible_drops)
        try:
            player.inventory.add_item(dropped_item)
        except Exception:
            try:
                player.inventory.items.append(dropped_item)
            except Exception:
                try:
                    player.inventory.append(dropped_item)
                except Exception:
                    pass
        name = getattr(dropped_item, "name", str(dropped_item))
        print(Fore.GREEN + f"🎁 {enemy.name} dropped {name}! Added to your inventory." + Style.RESET_ALL)

def game_loop():
    global player
    while True:
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + "⚔️  WELCOME TO THE RPG ADVENTURE  ⚔️".center(50) + Style.RESET_ALL)
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print(Fore.GREEN + "1. Start Game" + Style.RESET_ALL)
        print("2. Show Status")
        print("3. Choose Role")
        print("4. Shop 🛒")
        print("5. Inventory 🎒")
        print("6. Save Game 💾")
        print("7. Load Game 📂")
        print("8. Exit ❌")
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        try:
            choice = int(input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Invalid Choice!" + Style.RESET_ALL)
            continue

        if choice == 1:
            if player is None:
                name = input("Enter your name (or 'back' to return): ")
                if name.lower() == "back":
                    continue
                else:
                    player = Player(name)
                    print(Fore.GREEN + f"✨ Player {player.name} has been created!" + Style.RESET_ALL)
            else:
                print(Fore.CYAN + f"\nWelcome, {player.name}!\n" + Style.RESET_ALL)
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
                print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                print(Fore.RED + Style.BRIGHT + "👹 [Boss Fight]".center(50) + Style.RESET_ALL)
                battle(player, random_boss)
                if not player.is_alive():
                    player.defeated(random_boss)
                    player.hp = player.max_hp
                    player.status_effect = []
                    continue

                if not random_boss.is_alive():
                    random_boss.defeated(player)
                    print(Fore.GREEN + f"🏆 {random_boss.name} defeated! {player.name} wins!" + Style.RESET_ALL)
                    print(Fore.GREEN + f"+{random_boss.exp_reward} EXP earned.\n" + Style.RESET_ALL)
                    drop_item(player, random_boss, 0.8)

                # Last Boss
                Demon_Boss = Demon()
                print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                print(Fore.RED + Style.BRIGHT + "🔥 [Final Boss Fight] 🔥".center(50) + Style.RESET_ALL)
                battle(player, Demon_Boss)
                if not player.is_alive():
                    player.defeated(Demon_Boss)
                    player.hp = player.max_hp
                    player.status_effect = []
                    continue

                if not Demon_Boss.is_alive():
                    Demon_Boss.defeated(player)
                    print(Fore.GREEN + f"🏆 {Demon_Boss.name} defeated! {player.name} wins!" + Style.RESET_ALL)
                    print(Fore.GREEN + f"+{Demon_Boss.exp_reward} EXP earned.\n" + Style.RESET_ALL)
                    drop_item(player, Demon_Boss, 0.7)

        elif choice == 2:
            if player is not None:
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                print(Fore.CYAN + Style.BRIGHT + "📜 STATUS".center(50) + Style.RESET_ALL)
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                print(f"Name : {player.name}")
                print(f"HP   : {player.hp}")
                print(f"ATK  : {player.attack_power}")
                print(f"DEF  : {player.defense}")
                if player.equipped_weapon is not None :
                    print(f"Weapon : {player.equipped_weapon.name}")
                else :
                    print("Weapon : Unarmed")
                if player.equipped_armor is not None :
                    print(f"Armor  : {player.equipped_armor.name}")
                else :
                    print("Armor: Unarmored")
                print(f"Level: {player.level}")
                print(f"Exp: {player.exp} / {player.exp_needed}")
                print(f"Role: {player.role.name if player.role else 'None'}")
                print(f"Status Effect : {player.status_effects}")

            else:
                print(Fore.RED + "You don't have a character yet. Please create one first." + Style.RESET_ALL)

        elif choice == 3:
            if player:
                if player.level >= 5 and player.role is None:
                    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                    print(Fore.MAGENTA + Style.BRIGHT + "Choose your Role".center(50) + Style.RESET_ALL)
                    print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
                    print("1) Warrior")
                    print("2) Mage")
                    print("3) Archer")
                    print("4) Healer")
                    print("5) Back")
                    try:
                        choice_role = int(input("Select role number (or 5 to go back): "))
                    except ValueError:
                        print(Fore.RED + "Invalid Choice!" + Style.RESET_ALL)
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
                        print(Fore.RED + "Invalid role choice." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "You cannot choose a role yet." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Start the game first!" + Style.RESET_ALL)

        elif choice == 4:
            if player:
                while True:
                    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                    print(Fore.CYAN + Style.BRIGHT + "🛒 WELCOME TO THE SHOP".center(50) + Style.RESET_ALL)
                    print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                    print("1) Sword Shop")
                    print("2) Armor Shop")
                    print("3) Bow Shop")
                    print("4) Grimoire Shop")
                    print("5) Staff Shop")
                    print("6) Potion Shop")
                    print("7) Back")
                    print(f"💰 Your Coins: {player.coins}")
                    try:
                        shop_choice = int(input("Choose shop category: "))
                    except ValueError:
                        print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
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
                                player.inventory.add_item(selected)
                                selected["stock"] -= 1
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

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
                                player.inventory.add_item(selected)
                                selected["stock"] -= 1
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

                    elif shop_choice == 3:
                        bow_shop = shop_bow()
                        bow_shop.stock_tech_bow()
                        bow_shop.stock_crossbow()
                        bow_shop.stock_recuve_bow()
                        
                        bow_shop.show_items("🏹 Available Bows")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = bow_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.add_item(selected)
                                selected["stock"] -= 1
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

                    elif shop_choice == 4:
                        grimoire_shop = shop_grimoire()
                        grimoire_shop.stock_elemental_grimoire()
                        grimoire_shop.stock_dark_grimoire()
                        grimoire_shop.stock_arcane_grimoire()

                        grimoire_shop.show_items("📚 Available Grimoires")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = grimoire_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.add_item(selected)
                                selected["stock"] -= 1
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
                    
                    elif shop_choice == 5:
                        staff_shop = shop_staff()
                        staff_shop.stock_healing_staff()
                        staff_shop.stock_elemental_staff()
                        staff_shop.stock_dark_staff()

                        staff_shop.show_items("🔮 Available Staffs")

                        try:
                            buy_choice = int(input("Select item to buy (0 to cancel): "))
                            if buy_choice == 0:
                                continue
                            selected = staff_shop.inventory_shop[buy_choice - 1]
                            if player.coins >= selected["price"]:
                                player.coins -= selected["price"]
                                player.inventory.add_item(selected)
                                selected["stock"] -= 1
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

                    elif shop_choice == 6:
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
                                print(Fore.GREEN + f"\n✅ You bought {selected['name']}! It's added to your inventory." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)
                        except (ValueError, IndexError):
                            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
                        
                    elif shop_choice == 7:
                        print(Fore.YELLOW + "Exiting shop..." + Style.RESET_ALL)
                        break
            else:
                print(Fore.RED + "⚠️ Start the game first before visiting the shop!" + Style.RESET_ALL)

        elif choice == 5:
            inventory_menu()

        elif choice == 6:
            if player:
                save_games(player)
                print(Fore.GREEN + "💾 Game saved!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "No player to save!" + Style.RESET_ALL)

        elif choice == 7:
            player = load_game()
            print(Fore.GREEN + "📂 Game loaded!" + Style.RESET_ALL)

        elif choice == 8:
            print(Fore.YELLOW + "Exiting game..." + Style.RESET_ALL)
            break

    print(Fore.YELLOW + "="*56 + Style.RESET_ALL)
    print(Fore.CYAN + "| Thank you for playing the game".ljust(55) + "|" + Style.RESET_ALL)
    print(Fore.CYAN + "| Made By : Edbert Chandra, Kindy Lim, Louis Fortino".ljust(55) + "|" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*56 + Style.RESET_ALL)

if __name__ == "__main__":
    game_loop()