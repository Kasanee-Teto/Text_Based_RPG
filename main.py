"""
Main game loop for Text-Based RPG
Handles menu system, game flow, and player interactions
"""

from Character.Character_RPG import Player
from Character.Enemy_RPG import *
from items import *
from Character.Role import Warrior, Mage, Archer, Healer, Assassin
from save_game_RPG import save_game, load_game
from Shop import ShopFacade
from dungeon import Dungeon
from config import GameConfig

from colorama import Fore, Style, init
init(autoreset=True)

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

import time
import random
from typing import Optional


# ==============================
# GLOBAL STATE
# ==============================

console = Console()
player: Optional[Player] = None


# ==============================
# UI FUNCTIONS
# ==============================

def print_header(text: str, style: str = "cyan"):
    """
    Print a formatted header
    
    Args:
        text: Header text
        style: Color style (cyan, yellow, red, etc.)
    """
    separator = "=" * GameConfig.SEPARATOR_LENGTH
    print(Fore.YELLOW + separator + Style.RESET_ALL)
    print(getattr(Fore, style. upper()) + Style.BRIGHT + text. center(GameConfig.SEPARATOR_LENGTH) + Style.RESET_ALL)
    print(Fore.YELLOW + separator + Style. RESET_ALL)


def print_separator():
    """Print a simple separator line"""
    print(Fore. YELLOW + "-" * GameConfig.SEPARATOR_LENGTH + Style.RESET_ALL)


def show_loading_screen():
    """Display animated loading screen with progress bar"""
    console.clear()
    
    title = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   ██████╗ ██████╗  ██████╗                            ║
    ║   ██╔══██╗██╔══██╗██╔════╝                            ║
    ║   ██████╔╝██████╔╝██║  ███╗                           ║
    ║   ██╔══██╗██╔═══╝ ██║   ██║                           ║
    ║   ██║  ██║██║     ╚██████╔╝                           ║
    ║   ╚═╝  ╚═╝╚═╝      ╚═════╝                            ║
    ║                                                       ║
    ║        A D V E N T U R E   A W A I T S                ║
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
            time.sleep(random.uniform(GameConfig.LOADING_DELAY_MIN, GameConfig.LOADING_DELAY_MAX))
            progress.advance(task)
    
    console.print("\n")
    success_panel = Panel(
        Text("✨ Game loaded successfully!  ✨", justify="center", style="bold green"),
        border_style="green",
        padding=(1, 2)
    )
    console.print(success_panel)
    time.sleep(1)
    console.clear()


def display_status(player: Player):
    """
    Display player status in a formatted table
    
    Args:
        player: Player to display stats for
    """
    print_separator()
    print(Fore. CYAN + Style.BRIGHT + "📜 CHARACTER STATUS". center(GameConfig.SEPARATOR_LENGTH) + Style.RESET_ALL)
    print_separator()
    
    table = Table(show_header=False, box=None)
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="white")
    
    stats = player.get_stats_display()
    
    table.add_row("Name", stats['name'])
    table.add_row("HP", f"{stats['hp']}/{stats['max_hp']}")
    table.add_row("ATK", str(stats['attack']))
    table.add_row("DEF", str(stats['defense']))
    table.add_row("Weapon", stats['weapon'])
    table.add_row("Armor", stats['armor'])
    table.add_row("Level", str(stats['level']))
    table.add_row("EXP", stats['exp'])
    table.add_row("Coins", f"💰 {stats['coins']}")
    table.add_row("Role", stats['role'])
    table.add_row("Status Effects", str(stats['status_effects']) if stats['status_effects'] else "None")
    
    console.print(table)
    print_separator()


# ==============================
# GAME SYSTEMS
# ==============================

def battle(player: Player, enemy):
    """
    Handle turn-based combat between player and enemy
    
    Args:
        player: Player character
        enemy: Enemy character
    """
    print_header(f"⚔️  {player.name} VS {enemy.name}", "red")
    
    while player.is_alive() and enemy.is_alive():
        print(Fore.CYAN + "\n[Enter] Attack | [E] Inventory | [F] Status" + Style.RESET_ALL)
        choice = input(Fore.CYAN + "➤ " + Style.RESET_ALL).strip(). lower()
        
        if choice == 'e':
            inventory_menu()
            continue
        elif choice == 'f':
            display_status(player)
            continue
        
        # Player attacks
        player. attack(enemy)
        print_separator()
        
        # Check if enemy died
        if not enemy.is_alive():
            break
        
        # Enemy attacks back
        enemy.attack(player)
        
        # Apply status effects to player
        player.update_status_effects()
        
        # Display HP bars
        print(Fore.GREEN + f"💚 {player.name} HP: {player.hp}/{player.max_hp}" + Style.RESET_ALL)
        print(Fore.RED + f"💔 {enemy.name} HP: {enemy.hp}/{enemy.max_hp}" + Style.RESET_ALL)
        print_separator()
    
    # Level up check after battle
    if player.is_alive():
        player.level_up()


def drop_item(player: Player, enemy, drop_chance: float = 0.5):
    """
    Randomly drop items from defeated enemy
    
    Args:
        player: Player to receive items
        enemy: Defeated enemy
        drop_chance: Probability of drop (0.0 to 1.0)
    """
    if random.random() < drop_chance:
        possible_drops = [
            Short_Sword, Short_bow, Long_Sword, Mace,
            Wizards_Robe, Leather_Armor,
            Small_HPotion, Medium_HPotion
        ]
        dropped_item = random.choice(possible_drops)
        
        # Try to add to inventory
        if player.inventory.add_item(dropped_item):
            item_name = dropped_item.name
            print(Fore.GREEN + f"🎁 {enemy.name} dropped {item_name}!" + Style.RESET_ALL)


def inventory_menu():
    """Interactive inventory management menu"""
    global player
    
    if player is None:
        print(Fore.RED + "⚠️  Create a character first!" + Style. RESET_ALL)
        return
    
    if not player.inventory.items:
        print(Fore. YELLOW + "📦 Inventory is empty!" + Style.RESET_ALL)
        return
    
    running = True
    
    while running:
        if not player.inventory.items:
            print(Fore.YELLOW + "📦 Inventory is now empty!  Closing menu..." + Style.RESET_ALL)
            break
        
        print_header("🎒 INVENTORY MENU", "magenta")
        print("1) Show Inventory")
        print("2) Drop Item")
        print("3) Equip / Use Item")
        print("4) Show Item Description")
        print("5) Sort Inventory")
        print("6) Exit Inventory")
        print_separator()
        
        try:
            inv_choice = int(input(Fore.CYAN + "➤ Choose Action: " + Style.RESET_ALL))
            
            if inv_choice == 1:
                # Show inventory
                print_separator()
                player.inventory.list_items()
                print_separator()
            
            elif inv_choice == 2:
                # Drop item
                player.inventory.list_items()
                idx = int(input("➤ Choose item's index to remove: "))
                selected_item = player.inventory.get_item_by_index(idx)
                if selected_item:
                    player.inventory.remove_item(selected_item)
                    print(Fore.GREEN + "✅ Item removed." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "❌ Invalid index!" + Style.RESET_ALL)
            
            elif inv_choice == 3:
                # Equip/use item
                print_separator()
                print("Choose an item to equip/use:")
                player.inventory.list_items()
                print_separator()
                
                try:
                    item_choice = int(input("➤ Enter the item number (or 0 to cancel): "))
                    if item_choice == 0:
                        continue
                    
                    selected_item = player.inventory.get_item_by_index(item_choice)
                    
                    if selected_item is None:
                        print(Fore.RED + "❌ Invalid choice!" + Style.RESET_ALL)
                        continue
                    
                    if isinstance(selected_item, Health_Potions):
                        player.inventory.use_consumable(selected_item, player)
                        print(Fore.GREEN + "🧪 Potion used!" + Style.RESET_ALL)
                    elif isinstance(selected_item, Weapon):
                        player.equip_weapon(selected_item)
                        print(Fore. GREEN + "⚔️  Weapon equipped!" + Style. RESET_ALL)
                    elif isinstance(selected_item, Armor):
                        player.equip_armor(selected_item)
                        print(Fore.GREEN + "🛡️  Armor equipped!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "❌ This item cannot be used." + Style.RESET_ALL)
                
                except (ValueError, IndexError):
                    print(Fore.RED + "❌ Invalid choice!" + Style.RESET_ALL)
            
            elif inv_choice == 4:
                # Show item description
                player.inventory.list_items()
                idx = int(input("➤ Enter item's index: "))
                selected_item = player.inventory.get_item_by_index(idx)
                
                if selected_item:
                    print_separator()
                    # Use get_description method if available (Open-Closed Principle)
                    if hasattr(selected_item, 'get_description'):
                        print(selected_item.get_description())
                    else:
                        # Fallback for items without get_description
                        stats = []
                        for attr in ["damage", "defense", "heals"]:
                            if hasattr(selected_item, attr):
                                stats.append(f"{attr.title()}: +{getattr(selected_item, attr)}")
                        
                        stat_text = " | ".join(stats) if stats else "No Bonus"
                        rarity = getattr(selected_item, "rarity", "Common")
                        print(f"{selected_item.name} | {stat_text} | 💰 {selected_item.value} | {rarity}")
                    print_separator()
                else:
                    print(Fore.RED + "❌ Invalid index!" + Style.RESET_ALL)
            
            elif inv_choice == 5:
                # Sort inventory
                print("Sort by: 1) Name 2) Value")
                sort_choice = int(input("➤ Choose sorting method: "))
                if sort_choice == 1:
                    player.inventory.sort_items(by_name=True)
                    print(Fore.GREEN + "✅ Inventory sorted by name." + Style.RESET_ALL)
                elif sort_choice == 2:
                    player.inventory.sort_items(by_name=False)
                    print(Fore.GREEN + "✅ Inventory sorted by value." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "❌ Invalid sorting choice!" + Style.RESET_ALL)
            
            elif inv_choice == 6:
                # Exit
                running = False
                print(Fore.YELLOW + "Closing inventory..." + Style.RESET_ALL)
        
        except (ValueError, IndexError):
            print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)

def role_selection_menu():
    """Handle role/class selection for player"""
    global player
    
    if player is None:
        print(Fore.RED + "⚠️  Start the game first!" + Style.RESET_ALL)
        return
    
    if player.level < GameConfig.ROLE_UNLOCK_LEVEL:
        print(Fore.RED + f"⚠️  You need to be level {GameConfig.ROLE_UNLOCK_LEVEL} to choose a role!  (Current: {player.level})" + Style.RESET_ALL)
        return
    
    if player.role is not None:
        print(Fore.YELLOW + f"ℹ️  You already have a role: {player.role.__class__.__name__}" + Style.RESET_ALL)
        return
    
    print_header("🎭 CHOOSE YOUR ROLE", "magenta")
    print("1) Warrior  - High defense and HP tank")
    print("2) Mage     - Maximum attack, low defense")
    print("3) Archer   - Balanced ranged fighter")
    print("4) Healer   - Support with modest bonuses")
    print("5) Assasin  - High Attack, low defense")
    print("5) Assasin  - High damage, low defense")
    print("6) Back")
    print_separator()
    
    try:
        choice_role = int(input(Fore.CYAN + "➤ Select role number: " + Style.RESET_ALL))
        
        role_map = {
            1: Warrior,
            2: Mage,
            3: Archer,
            4: Healer,
            5: Assassin
        }
        
        if choice_role == 6:
            return
        
        role_class = role_map.get(choice_role)
        if role_class:
            player.choose_role(role_class())
        else:
            print(Fore.RED + "❌ Invalid role choice." + Style.RESET_ALL)
    
    except ValueError:
        print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)


def combat_scenario():
    """Run a standard combat scenario with random enemies and bosses"""
    global player
    
    if player is None:
        print(Fore.RED + "⚠️  Create a character first!" + Style.RESET_ALL)
        return
    
    print(Fore.CYAN + f"\n🌟 Welcome, {player.name}!\n" + Style.RESET_ALL)
    
    # Normal enemy encounter
    enemy_list = [Goblin_Grunt, Spider, Skeleton, Zombie]
    random_enemy = random.choice(enemy_list)
    battle(player, random_enemy)
    
    if not random_enemy.is_alive():
        random_enemy.defeated(player)
        drop_item(player, random_enemy, GameConfig.NORMAL_DROP_CHANCE)
    
    if not player.is_alive():
        player.defeated(random_enemy)
        player.hp = player.max_hp
        player.status_effects = []
        return
    
    # Boss encounter
    boss_list = [Wolf(), Ogre(), Vampire()]
    random_boss = random. choice(boss_list)
    print_header("👹 BOSS FIGHT", "red")
    battle(player, random_boss)
    
    if not player.is_alive():
        player.defeated(random_boss)
        player.hp = player.max_hp
        player.status_effects = []
        return
    
    if not random_boss.is_alive():
        random_boss.defeated(player)
        print(Fore.GREEN + f"🏆 {random_boss.name} defeated! {player.name} wins!" + Style.RESET_ALL)
        drop_item(player, random_boss, GameConfig. BOSS_DROP_CHANCE)
    
    # Final boss
    demon_boss = Demon()
    print_header("🔥 FINAL BOSS FIGHT 🔥", "red")
    battle(player, demon_boss)
    
    if not player.is_alive():
        player.defeated(demon_boss)
        player.hp = player.max_hp
        player.status_effects = []
        return
    
    if not demon_boss.is_alive():
        demon_boss. defeated(player)
        print(Fore.GREEN + Style.BRIGHT + "🎉 CONGRATULATIONS! YOU DEFEATED THE DEMON KING!  🎉" + Style. RESET_ALL)
        drop_item(player, demon_boss, GameConfig.FINAL_BOSS_DROP_CHANCE)


def dungeon_mode():
    """Enter procedurally generated dungeon"""
    global player
    
    if player is None:
        print(Fore.RED + "⚠️  Create a character first!" + Style.RESET_ALL)
        return
    
    print_header("🏰 DUNGEON MODE", "magenta")
    print("Choose difficulty:")
    print("1) Easy   (0.8x difficulty)")
    print("2) Normal (1.0x difficulty)")
    print("3) Hard   (1.5x difficulty)")
    print("4) Back")
    
    try:
        diff_choice = int(input(Fore.CYAN + "➤ " + Style.RESET_ALL))
        
        difficulty_map = {1: 0.8, 2: 1.0, 3: 1.5}
        difficulty = difficulty_map.get(diff_choice)
        
        if difficulty is None:
            return
        
        # Generate dungeon
        dungeon = Dungeon(
            width=GameConfig.DEFAULT_DUNGEON_WIDTH,
            height=GameConfig.DEFAULT_DUNGEON_HEIGHT,
            depth=1,
            seed=None,
            difficulty=difficulty
        )
        
        print(Fore.YELLOW + "🏰 Entering dungeon..." + Style.RESET_ALL)
        success = dungeon.explore_from(player, battle)
        
        if not success:
            player.defeated(Enemy("Dungeon", 0, 0, 0, 0))
            player.hp = player.max_hp
            player.status_effects = []
    
    except ValueError:
        print(Fore.RED + "❌ Invalid input!" + Style. RESET_ALL)


# ==============================
# MAIN GAME LOOP
# ==============================

def game_loop():
    """Main game loop - central menu system"""
    global player
    
    while True:
        print_header("⚔️  WELCOME TO THE RPG ADVENTURE  ⚔️", "cyan")
        print(Fore.GREEN + "1. Start Game" + Style.RESET_ALL)
        print("2. Show Status")
        print("3. Choose Role")
        print("4. Shop 🛒")
        print("5. Inventory 🎒")
        print("6. Save Game 💾")
        print("7. Load Game 📂")
        print("8. Dungeon 🏰")
        print("9. Exit ❌")
        print_separator()
        
        try:
            choice = int(input(Fore.CYAN + "➤ Enter your choice: " + Style. RESET_ALL))
        except ValueError:
            print(Fore. RED + "❌ Invalid choice!" + Style.RESET_ALL)
            continue
        
        # ===== OPTION 1: Start Game =====
        if choice == 1:
            if player is None:
                name = input("➤ Enter your name (or 'back' to return): ")
                if name.lower() == "back":
                    continue
                player = Player(
                    name,
                    start_hp=GameConfig. PLAYER_START_HP,
                    start_attack=GameConfig.PLAYER_START_ATTACK,
                    start_defense=GameConfig.PLAYER_START_DEFENSE,
                    start_coins=GameConfig. PLAYER_START_COINS
                )
                print(Fore.GREEN + f"✨ Player {player.name} has been created!" + Style.RESET_ALL)
            else:
                combat_scenario()
        
        # ===== OPTION 2: Show Status =====
        elif choice == 2:
            if player is not None:
                display_status(player)
            else:
                print(Fore. RED + "⚠️  You don't have a character yet.  Please create one first." + Style.RESET_ALL)
        
        # ===== OPTION 3: Choose Role =====
        elif choice == 3:
            role_selection_menu()
        
        # ===== OPTION 4: Shop =====
        elif choice == 4:
            if player:
                shop_facade = ShopFacade()
                shopping = True
                
                while shopping:
                    shop_facade.display_shop_menu(player)
                    try:
                        shop_choice = int(input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL))
                        shopping = shop_facade.visit_shop(shop_choice, player)
                    except ValueError:
                        print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "⚠️ Start the game first before visiting the shop!" + Style.RESET_ALL)
                
        # ===== OPTION 5: Inventory =====
        elif choice == 5:
            inventory_menu()
        
        # ===== OPTION 6: Save Game =====
        elif choice == 6:
            if player:
                save_game(player)
            else:
                print(Fore.RED + "⚠️  No player to save!" + Style.RESET_ALL)
        
        # ===== OPTION 7: Load Game =====
        elif choice == 7:
            loaded_player = load_game()
            if loaded_player:
                player = loaded_player
                print(Fore.GREEN + f"✅ Welcome back, {player.name}!" + Style.RESET_ALL)
        
        # ===== OPTION 8: Dungeon =====
        elif choice == 8:
            dungeon_mode()
        
        # ===== OPTION 9: Exit =====
        elif choice == 9:
            print(Fore.YELLOW + "\n🎮 Exiting game..." + Style.RESET_ALL)
            break
        
        else:
            print(Fore. RED + "❌ Invalid choice!  Please choose 1-9." + Style. RESET_ALL)
    
    # Exit message
    print_header("👋 THANK YOU FOR PLAYING", "cyan")
    print(Fore.CYAN + "Made by: Edbert Chandra, Kindy Lim, Louis Fortino". center(GameConfig.SEPARATOR_LENGTH) + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * GameConfig.SEPARATOR_LENGTH + Style.RESET_ALL)


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    show_loading_screen()
    game_loop()