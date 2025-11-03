from Character.Character_RPG import Player
from Character.Enemy_RPG import *
from items import *
from Character.Role import Warrior, Mage, Archer, Healer
from save_game_RPG import save_games, load_game
from Shop import shop_bow, shop_sword, shop_armor, shop_potion, shop_grimoire, shop_staff
from dungeon import Dungeon

from colorama import Fore, Style, init
init(autoreset=True)

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
import time
import random

console = Console()
player = None

def show_loading_screen():
    console.clear()
    
    title = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   ██████╗ ██████╗  ██████╗                          ║
    ║   ██╔══██╗██╔══██╗██╔════╝                          ║
    ║   ██████╔╝██████╔╝██║  ███╗                         ║
    ║   ██╔══██╗██╔═══╝ ██║   ██║                         ║
    ║   ██║  ██║██║     ╚██████╔╝                         ║
    ║   ╚═╝  ╚═╝╚═╝      ╚═════╝                          ║
    ║                                                       ║
    ║        A D V E N T U R E   A W A I T S               ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    
    console.print(title, style="bold cyan")
    console.print("\n")
    
    # Loading messages
    loading_messages = [
        "Forging legendary weapons...",
        "Summoning ancient monsters...",
        "Preparing dungeon floors...",
        "Stocking the shop inventory...",
        "Brewing health potions...",
        "Enchanting armor sets...",
        "Rolling for loot...",
        "Initializing battle system...",
        "Loading save files...",
        "Generating random encounters..."
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        
        task = progress.add_task("[cyan]Loading game...", total=len(loading_messages))
        
        for msg in loading_messages:
            progress.update(task, description=f"[cyan]{msg}")
            time.sleep(random.uniform(0.2, 0.5))  
            progress.advance(task)
    
    console.print("\n")
    success_panel = Panel(
        Text("✨ Game loaded successfully! ✨", justify="center", style="bold green"),
        border_style="green",
        padding=(1, 2)
    )
    console.print(success_panel)
    time.sleep(1)
    console.clear()

def inventory_menu():
    global player
    running = True

    if player == None:
        print(Fore.RED + "⚠️  Create a character first!" + Style.RESET_ALL)
        running = False

    elif not player.inventory.items:
        print("Inventory is empty !")
        running = False

    while running:

        if not player.inventory.items:
            print("Inventory is empty ! Menu automatically closes")
            break

        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "🎒 INVENTORY MENU".center(50) + Style.RESET_ALL)
        print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
        print("1) Show Inventory")
        print("2) Drop Item")
        print("3) Equip / Use Item")
        print("4) Show Item Description")
        print("5) Sort Inventory")
        print("6) Exit Inventory")
        print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
        try:
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
                stats = []
                for attr in ["damage", "defense", "heals"]:
                    if hasattr(selected_item, attr):
                        stats.append(f"{attr.title()}: +{getattr(selected_item, attr)}")

                stat_text = " | ".join(stats) if stats else "No Bonus"
                print(
                    f"{selected_item.name}{Style.RESET_ALL} | {stat_text} | 💰 {selected_item.value} | {Style.RESET_ALL}"
                    )
                print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)

            elif inv_choice == 5 :
                print("Sort by: 1) Name 2) Value")
                sort_choice = int(input("Choose sorting method: "))
                if sort_choice == 1:
                    player.inventory.sort_items(by_name=True)
                    print(Fore.GREEN + "✅ Inventory sorted by name." + Style.RESET_ALL)
                elif sort_choice == 2:
                    player.inventory.sort_items(by_name=False)
                    print(Fore.GREEN + "✅ Inventory sorted by value." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid sorting choice!" + Style.RESET_ALL)
                    
            elif inv_choice == 6 :
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
        pilihan = input(Fore.CYAN + "\nPress Enter to Attack\nPress 'E' to open Inventory\nPress 'F' to show status\n=" + Style.RESET_ALL)
        if pilihan.lower() == 'e':
            inventory_menu()
        else :
            player.attack(enemy)
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
        if pilihan.lower() == 'f':
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
        print("8. Dungeon")
        print("9. Exit ❌")
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

                boss_list = [Wolf(), Ogre(), Vampire()]
                random_boss = random.choice(boss_list)
                print(Fore.YELLOW + "="*50 + Style.RESET_ALL)
                print(Fore.RED + Style.BRIGHT + "👹 [Boss Fight]".center(50) + Style.RESET_ALL)
                battle(player, random_boss)
                if not player.is_alive():
                    player.defeated(random_boss)
                    player.hp = player.max_hp
                    player.status_effect = []
                    player.status_effects.clear()
                    print(Fore.RED + f"{player.name} has fallen! Status effects removed." + Style.RESET_ALL)
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
                    player.status_effects.clear()
                    print(Fore.RED + f"{player.name} has fallen! Status effects removed." + Style.RESET_ALL)
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
                    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
                    print(Fore.CYAN + Style.BRIGHT + "🛒 WELCOME TO THE SHOP".center(50) + Style.RESET_ALL)
                    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
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

                    # === SHOP OBJECTS ===
                    shop_mapping = {
                        1: (shop_sword, ["stock_sword_dagger", "stock_sword_katana", "stock_sword_great_sword"], "⚔️ Sword Shop"),
                        2: (shop_armor, ["stock_armors"], "🛡️ Armor Shop"),
                        3: (shop_bow, ["stock_bows"], "🏹 Bow Shop"),
                        4: (shop_grimoire, ["stock_grimoires"], "📜 Grimoire Shop"),
                        5: (shop_staff, ["stock_staffs"], "💫 Staff Shop"),
                        6: (shop_potion, ["stock_health_potions"], "💊 Potion Shop")
                    }

                    if shop_choice == 7:
                        print(Fore.YELLOW + "Exiting shop..." + Style.RESET_ALL)
                        break

                    shop_class, methods, title = shop_mapping.get(shop_choice, (None, None, None))
                    if not shop_class:
                        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
                        continue

                    current_shop = shop_class()
                    for m in methods:
                        getattr(current_shop, m)()
                    current_shop.show_items(title)

                    try:
                        buy_choice = int(input("Select item to buy (0 to cancel): "))
                        if buy_choice == 0:
                            continue

                        selected_item = current_shop.inventory_shop[buy_choice - 1]
                        price = getattr(selected_item, "value", 0)

                        if player.coins >= price:
                            player.coins -= price
                            player.inventory.add_item(selected_item)
                            print(Fore.GREEN + f"\n✅ You bought {selected_item.name}! Added to inventory." + Style.RESET_ALL)
                        else:
                            print(Fore.RED + "❌ Not enough coins!" + Style.RESET_ALL)

                    except (ValueError, IndexError):
                        print(Fore.RED + "Invalid selection!" + Style.RESET_ALL)
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
            if player is None:
                print("Create a character first!")
            else:
                d = Dungeon(width=5, height=5, depth=1, seed=None, difficulty=1.0)
                print("Entering dungeon floor 1...")
                success = d.explore_from(player, battle)
                if not success:
                    player.defeated(Demon() if False else Enemy("TrapDeath",0,0,0,0))  # just print; optional
                    player.hp = player.max_hp
                    player.status_effect = []

        elif choice == 9:
            print(Fore.YELLOW + "Exiting game..." + Style.RESET_ALL)
            break

    print(Fore.YELLOW + "="*56 + Style.RESET_ALL)
    print(Fore.CYAN + "| Thank you for playing the game".ljust(55) + "|" + Style.RESET_ALL)
    print(Fore.CYAN + "| Made By : Edbert Chandra, Kindy Lim, Louis Fortino".ljust(55) + "|" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*56 + Style.RESET_ALL)

if __name__ == "__main__":
    show_loading_screen() 
    game_loop()