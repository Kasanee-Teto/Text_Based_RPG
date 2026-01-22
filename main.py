"""
Main game loop for Text-Based RPG.
"""
import time
import random
from typing import Optional

from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Local Imports - NESTED STRUCTURE
from Character.Character_RPG import Player
from Character.Enemy_RPG import GoblinGrunt, CaveSpider, Skeleton, Zombie, Enemy
from items import HealthPotion, Weapon, Armor
from Character.Role import Warrior, Mage, Archer, Healer, Assassin
from save_game_RPG import save_game, load_game
from Shop import ShopFacade
from dungeon import Dungeon
from config import CONFIG

init(autoreset=True)
console = Console()
player: Optional[Player] = None

# ==============================
# UI HELPERS
# ==============================

def print_header(text: str, style: str = "cyan"):
    """
    Print a formatted header
    
    Args:
        text: Header text
        style: Color style (cyan, yellow, red, etc.)
    """
    """Print a formatted header matching original design."""
    separator = "=" * CONFIG.UI.SEPARATOR_LENGTH
    print(Fore.YELLOW + separator + Style.RESET_ALL)
    print(getattr(Fore, style.upper()) + Style.BRIGHT + text.center(CONFIG.UI.SEPARATOR_LENGTH) + Style.RESET_ALL)
    print(Fore.YELLOW + separator + Style.RESET_ALL)

def print_separator():
    """Print a simple separator line."""
    print(Fore.YELLOW + "-" * CONFIG.UI.SEPARATOR_LENGTH + Style.RESET_ALL)

def show_loading_screen():
    """Display animated loading screen with progress bar (Original UI)."""
    console.clear()
    
    title = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   ██████╗ ██████╗  ██████╗                            ║
    ║   ██╔══██╗██╔══██╗██╔════╝                            ║
    ║   ██████╔╝████���█╔╝██║  ███╗                           ║
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
            time.sleep(random.uniform(CONFIG.UI.LOADING_DELAY_MIN, CONFIG.UI.LOADING_DELAY_MAX))
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

def read_int(prompt: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    try:
        val = int(input(Fore.CYAN + prompt + Style.RESET_ALL))
        if min_val is not None and val < min_val: return None
        if max_val is not None and val > max_val: return None
        return val
    except ValueError:
        return None

# ==============================
# GAME LOGIC HELPERS
# ==============================

def battle(player_char: Player, enemy: Enemy):
    print_header(f"⚔️  {player_char.name} VS {enemy.name}", "red")
    
    while player_char.is_alive() and enemy.is_alive():
        print(Fore.CYAN + "\n[Enter] Attack | [E] Inventory | [F] Status" + Style.RESET_ALL)
        choice = input(Fore.CYAN + "➤ " + Style.RESET_ALL).strip().lower()
        
        if choice == 'e':
            _handle_inventory_logic()
            continue
        elif choice == 'f':
            display_status(player_char)
            continue
        
        player_char.attack(enemy)
        print_separator()
        
        if enemy.is_alive():
            enemy.attack(player_char)
            player_char.update_status_effects()
        
        print(Fore.GREEN + f"💚 {player_char.name} HP: {player_char.hp}/{player_char.max_hp}")
        print(Fore.RED + f"💔 {enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
        print_separator()
    
    if player_char.is_alive():
        player_char.level_up()

def display_status(p: Player):
    print_separator()
    print(Fore.CYAN + Style.BRIGHT + "📜 CHARACTER STATUS".center(CONFIG.UI.SEPARATOR_LENGTH))
    
    table = Table(show_header=False, box=None)
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="white")
    
    stats = p.get_stats_display()
    for k, v in stats.items():
        table.add_row(k.title(), str(v))
    
    console.print(table)
    print_separator()

# ==============================
# SUB-MENUS
# ==============================

def _handle_inventory_logic():
    if not player:
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
    
    handlers = {
        1: lambda: player.inventory.list_items(),
        2: _inv_drop_item,
        3: _inv_equip_use,
        4: _inv_show_desc,
        5: _inv_sort,
    }
    
    while True:
        if not player.inventory.items:
            print(Fore.YELLOW + CONFIG.UI.MSG_INVENTORY_EMPTY)
            break
            
        print_header("🎒 INVENTORY MENU", "magenta")
        print("1) Show Inventory")
        print("2) Drop Item")
        print("3) Equip / Use Item")
        print("4) Show Item Description")
        print("5) Sort Inventory")
        print("6) Exit Inventory")
        print_separator()
        
        choice = read_int("➤ Choose Action: ", 1, 6)
        if choice == 6 or choice is None:
            print(Fore.YELLOW + "Closing inventory..." + Style.RESET_ALL)
            break
            
        handlers.get(choice, lambda: print(CONFIG.UI.MSG_INVALID_CHOICE))()

def _inv_drop_item():
    player.inventory.list_items()
    idx = read_int("➤ Choose item's index to remove: ")
    if idx:
        item = player.inventory.get_item_by_index(idx)
        if item:
            player.inventory.remove_item(item)
            print(Fore.GREEN + "✅ Item removed.")

def _inv_equip_use():
    player.inventory.list_items()
    idx = read_int("➤ Enter the item number (or 0 to cancel): ")
    if not idx: return
    
    item = player.inventory.get_item_by_index(idx)
    if not item: return

    if isinstance(item, HealthPotion):
        if player.inventory.use_consumable(item, player):
            print(Fore.GREEN + "🧪 Potion used!")
    elif isinstance(item, Weapon):
        player.equip_weapon(item)
        print(Fore.GREEN + "⚔️  Weapon equipped!")
    elif isinstance(item, Armor):
        player.equip_armor(item)
        print(Fore.GREEN + "🛡️  Armor equipped!")
    else:
        print(Fore.RED + "❌ This item cannot be used.")

def _inv_show_desc():
    player.inventory.list_items()
    idx = read_int("➤ Enter item's index: ")
    item = player.inventory.get_item_by_index(idx) if idx else None
    if item:
        print(f"{item.name} | Val: {item.value} | {getattr(item, 'rarity', 'Common')}")

def _inv_sort():
    choice = read_int("1) Name 2) Value: ", 1, 2)
    if choice == 1: 
        player.inventory.sort_items(True)
        print(Fore.GREEN + "✅ Inventory sorted by name.")
    elif choice == 2: 
        player.inventory.sort_items(False)
        print(Fore.GREEN + "✅ Inventory sorted by value.")

# ==============================
# MAIN HANDLERS
# ==============================

def _handle_start_game():
    global player
    if player is None:
        name = input("➤ Enter your name (or 'back' to return): ")
        if name.lower() == "back": return
        player = Player(name)
        print(Fore.GREEN + f"✨ Player {player.name} has been created!")
    else:
        enemy = random.choice([GoblinGrunt(), CaveSpider(), Skeleton(), Zombie()])
        battle(player, enemy)
        if not player.is_alive():
             player.defeated(enemy)
             player.hp = player.max_hp

def _handle_shop():
    if not player:
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
    facade = ShopFacade()
    facade.display_shop_menu(player)
    
    while True:
        choice = read_int("➤ Enter your choice: ", 1, 7)
        if not choice: break
        
        if not facade.visit_shop(choice, player):
            break
        
        # Redisplay menu after returning from a specific shop
        facade.display_shop_menu(player)

def _handle_dungeon():
    if not player:
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
        
    print_header("🏰 DUNGEON MODE", "magenta")
    print("Choose difficulty:")
    print("1) Easy   (0.8x difficulty)")
    print("2) Normal (1.0x difficulty)")
    print("3) Hard   (1.5x difficulty)")
    
    diff_map = {1: 0.8, 2: 1.0, 3: 1.5}
    choice = read_int("➤ ", 1, 3)
    if not choice: return
    
    dungeon = Dungeon(difficulty=diff_map[choice])
    print(Fore.YELLOW + "🏰 Entering dungeon..." + Style.RESET_ALL)
    
    if not dungeon.explore_from(player, battle):
        player.defeated(Enemy("Dungeon", 0,0,0,0))
        player.hp = player.max_hp

def _handle_role():
    if not player: 
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
    if player.level < CONFIG.PLAYER.ROLE_UNLOCK_LEVEL:
        print(Fore.RED + f"⚠️  Need level {CONFIG.PLAYER.ROLE_UNLOCK_LEVEL}!" + Style.RESET_ALL)
        return
    if player.role:
        print(Fore.YELLOW + "ℹ️  You already have a role." + Style.RESET_ALL)
        return
        
    roles = {1: Warrior, 2: Mage, 3: Archer, 4: Healer, 5: Assassin}
    print_header("🎭 CHOOSE YOUR ROLE", "magenta")
    print("1) Warrior  - High defense and HP tank")
    print("2) Mage     - Maximum attack, low defense")
    print("3) Archer   - Balanced ranged fighter")
    print("4) Healer   - Support with modest bonuses")
    print("5) Assassin - High Attack, low defense")
    print("6) Back")
    
    choice = read_int("➤ Select role number: ", 1, 6)
    if choice and choice != 6: 
        player.choose_role(roles[choice]())

def _handle_save():
    if player: save_game(player)
    else: print(Fore.RED + "⚠️  No player to save!" + Style.RESET_ALL)

def _handle_load():
    global player
    loaded = load_game()
    if loaded: 
        player = loaded
        print(Fore.GREEN + f"✅ Welcome back, {player.name}!")

def _handle_status():
    if player: display_status(player)
    else: print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)

# ==============================
# MAIN LOOP
# ==============================

def game_loop():
    handlers = {
        1: _handle_start_game,
        2: _handle_status,
        3: _handle_role,
        4: _handle_shop,
        5: _handle_inventory_logic,
        6: _handle_save,
        7: _handle_load,
        8: _handle_dungeon,
    }
    
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
        
        choice = read_int("➤ Enter your choice: ", 1, 9)
        
        if choice == 9: 
            print(Fore.YELLOW + "\n🎮 Exiting game..." + Style.RESET_ALL)
            print_header("👋 THANK YOU FOR PLAYING", "cyan")
            break
            
        if choice in handlers:
            handlers[choice]()
        else:
            print(CONFIG.UI.MSG_INVALID_CHOICE)

if __name__ == "__main__":
    show_loading_screen()
    game_loop()