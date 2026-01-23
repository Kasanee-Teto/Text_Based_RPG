"""
Main game loop for Text-Based RPG.
Refactored to act as Composition Root, wiring dependencies for Dungeon and Shop.
"""
import time
import random
from typing import Optional, List, Dict, Any

from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from Character.Character_RPG import Player
from Character.Enemy_RPG import GoblinGrunt, CaveSpider, Skeleton, Zombie, Enemy, WolfBoss, OgreBoss, VampireBoss, DemonBoss
from items import (HealthPotion, Weapon, Armor, ShortSword, ShortBow, LongSword, Mace,
                   WizardsRobe, LeatherArmor, IronArmor, SmallHPotion, MediumHPotion, LargeHPotion, XLHPotion, Item)
from Character.Role import Warrior, Mage, Archer, Healer, Assassin
from save_game_RPG import save_game, load_game
from Shop import ShopFacade
from dungeon import Dungeon, DungeonPresenter, SpawnStrategy
from config import CONFIG

init(autoreset=True)
console = Console()
player: Optional[Player] = None

# ==============================
# CONCRETE IMPLEMENTATIONS (DIP)
# ==============================

class ConsoleDungeonPresenter:
    """Concrete UI implementation for Dungeon."""
    
    def show_entrance_msg(self, depth: int):
        print("\n" + "=" * 50)
        print(f"🏰 Entering Dungeon Depth {depth}...".center(50))
        print("=" * 50)

    def show_exit_msg(self, reward: int):
        print("\n" + "=" * 50)
        print("🎉 You unlocked the exit and descend deeper!".center(50))
        print(f"💰 You collected {reward} coins.")

    def show_room(self, room_desc: str, room_summary: str, map_str: str, x: int, y: int, has_key: bool):
        print("\n--- Dungeon Map ---")
        print(map_str)
        print(f"\n📍 Position: ({x},{y})")
        if has_key:
            print(Fore.YELLOW + "🔑 Key Status: COLLECTED" + Style.RESET_ALL)
        else:
            print(Fore.RED + "🔑 Key Status: MISSING" + Style.RESET_ALL)
        print(f"   {room_desc}")
        print(f"   {room_summary}")

    def show_trap_trigger(self, trap_name: str, damage: int, player_name: str, status: Optional[str]):
        print(f"\n⚠️ Trap triggered: {trap_name}!")
        print(f"💥 {player_name} took {damage} damage!")
        if status:
            print(f"😵 {player_name} is afflicted with {status}.")

    def show_combat_start(self, enemy_name: str):
        print(f"\n⚔️ An enemy appears: {enemy_name}!")

    def show_treasure_found(self, item_name: str):
        print(f"💎 You discovered treasure: {item_name}")

    def show_retreat_msg(self):
        print("🚪 You retreat from the dungeon.")

    def show_key_found(self):
        print(Fore.YELLOW + Style.BRIGHT + "\n🗝️  YOU FOUND THE DUNGEON KEY!  🗝️" + Style.RESET_ALL)
        print("You can now open the exit door.")

    def show_exit_locked(self):
        print(Fore.RED + "\n🔒 THE EXIT IS LOCKED!" + Style.RESET_ALL)
        print("You must find the Key hidden somewhere in this level.")

    def show_game_complete(self):
        print("\n" + Fore.YELLOW + "=" * 50)
        print("🏆  CONGRATULATIONS!  🏆".center(50))
        print("=" * 50)
        print("You have defeated the Demon King and cleared Depth 20!")
        print("The world is safe once more.")
        print("=" * 50 + Style.RESET_ALL)

    def get_movement_input(self, available_moves: List[str]) -> Optional[str]:
        print("\n🧭 Available moves:", ", ".join(available_moves) + " | (Q)uit")
        choice = input("➤ Move (N/S/E/W) or Q: ").strip().lower()
        return choice

class GameSpawnStrategy:
    """Concrete strategy for spawning game entities based on depth."""
    
    def create_enemy(self, depth: int) -> Any:
        # Scale enemy types slightly with depth
        choice = random.random()
        if depth < 5:
            if choice < 0.4: enemy = CaveSpider()
            elif choice < 0.8: enemy = GoblinGrunt()
            else: enemy = Skeleton()
        elif depth < 10:
            if choice < 0.3: enemy = GoblinGrunt()
            elif choice < 0.6: enemy = Skeleton()
            else: enemy = Zombie()
        else:
            # Harder enemies appear more often deep down
            if choice < 0.2: enemy = Skeleton()
            else: enemy = Zombie()
            
        return enemy

    def create_boss(self, depth: int) -> Any:
        # Depth determines specific boss difficulty tiers if we had them,
        # for now random pool but scaled in Dungeon class
        boss = random.choice([WolfBoss(), OgreBoss(), VampireBoss()])
        return boss

    def create_final_boss(self, depth: int) -> Any:
        return DemonBoss()

    def create_loot(self) -> Item:
        loot_pool = [SmallHPotion, MediumHPotion, ShortSword, ShortBow, WizardsRobe, LeatherArmor]
        return random.choice(loot_pool)

    def create_trap(self) -> Dict[str, Any]:
        trap_types = [
            {"name": "spike trap", "damage": 8},
            {"name": "poison needle", "damage": 5, "status": "weakened"},
            {"name": "falling rocks", "damage": 12},
        ]
        return random.choice(trap_types)

# ==============================
# UI HELPERS (Unchanged)
# ==============================

def print_header(text: str, style: str = "cyan"):
    separator = "=" * CONFIG.UI.SEPARATOR_LENGTH
    print(Fore.YELLOW + separator + Style.RESET_ALL)
    print(getattr(Fore, style.upper()) + Style.BRIGHT + text.center(CONFIG.UI.SEPARATOR_LENGTH) + Style.RESET_ALL)
    print(Fore.YELLOW + separator + Style.RESET_ALL)

def print_separator():
    print(Fore.YELLOW + "-" * CONFIG.UI.SEPARATOR_LENGTH + Style.RESET_ALL)

def show_loading_screen():
    # ... (Keep existing implementation) ...
    pass 

def read_int(prompt: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    # ... (Keep existing implementation) ...
    try:
        val = int(input(Fore.CYAN + prompt + Style.RESET_ALL))
        if min_val is not None and val < min_val: return None
        if max_val is not None and val > max_val: return None
        return val
    except ValueError:
        return None

# ==============================
# GAME LOGIC HELPERS (Unchanged)
# ==============================

def _drop_loot(player_char: Player, enemy: Enemy):
    # ... (Keep existing implementation) ...
    is_boss = isinstance(enemy, (WolfBoss, OgreBoss, VampireBoss))
    is_demon = isinstance(enemy, DemonBoss)
    
    if is_demon: drop_chance = CONFIG.DROP_CHANCE_FINAL_BOSS
    elif is_boss: drop_chance = CONFIG.DROP_CHANCE_BOSS
    else: drop_chance = CONFIG.DROP_CHANCE_NORMAL
    
    if random.random() <= drop_chance:
        if is_demon: loot_pool = [IronArmor, LongSword, XLHPotion, LargeHPotion]
        elif is_boss: loot_pool = [LongSword, Mace, WizardsRobe, LeatherArmor, LargeHPotion, MediumHPotion]
        else: loot_pool = [ShortSword, ShortBow, LeatherArmor, SmallHPotion, MediumHPotion]
        
        dropped_item = random.choice(loot_pool)
        player_char.inventory.add_item(dropped_item)
        print(Fore.GREEN + f"💎 {enemy.name} dropped: {dropped_item.name}!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"💨 {enemy.name} dropped nothing." + Style.RESET_ALL)

def battle(player_char: Player, enemy: Enemy):
    # ... (Keep existing implementation) ...
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
        enemy.defeated(player_char)
        player_char.level_up()
        _drop_loot(player_char, enemy)

def display_status(p: Player):
    print_separator()
    print(Fore.CYAN + Style.BRIGHT + "📜 CHARACTER STATUS".center(CONFIG.UI.SEPARATOR_LENGTH))
    table = Table(show_header=False, box=None)
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="white")
    
    stats = p.get_stats_display()
    # Add Depth to status display
    table.add_row("Current Depth", str(p.current_depth if hasattr(p, 'current_depth') else 1))
    
    for k, v in stats.items():
        table.add_row(k.title(), str(v))
    console.print(table)
    print_separator()

# ==============================
# SUB-MENUS (Unchanged except Inventory)
# ==============================

def _handle_inventory_logic():
    # ... (Keep existing implementation) ...
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
        print("1) Show Inventory\n2) Drop Item\n3) Equip / Use Item\n4) Show Item Description\n5) Sort Inventory\n6) Exit Inventory")
        print_separator()
        choice = read_int("➤ Choose Action: ", 1, 6)
        if choice == 6 or choice is None: break
        handlers.get(choice, lambda: print(CONFIG.UI.MSG_INVALID_CHOICE))()

def _inv_drop_item():
    # ... (Keep existing implementation) ...
    player.inventory.list_items()
    idx = read_int("➤ Choose item's index to remove: ")
    if idx:
        item = player.inventory.get_item_by_index(idx)
        if item: player.inventory.remove_item(item)

def _inv_equip_use():
    # ... (Keep existing implementation) ...
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
    # ... (Keep existing implementation) ...
    player.inventory.list_items()
    idx = read_int("➤ Enter item's index: ")
    item = player.inventory.get_item_by_index(idx) if idx else None
    if item: print(f"ℹ️  {item.get_description()}")

def _inv_sort():
    # ... (Keep existing implementation) ...
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
        # Ensure new player starts at depth 1
        player = Player(name)
        player.current_depth = 1 
        print(Fore.GREEN + f"✨ Player {player.name} has been created!")
    else:
        print(Fore.YELLOW + "ℹ️  Player already exists! Go to Dungeon to continue your journey." + Style.RESET_ALL)

def _handle_shop():
    # ... (Keep existing implementation) ...
    if not player:
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
    facade = ShopFacade()
    facade.display_shop_menu(player)
    while True:
        choice = read_int("➤ Enter your choice: ", 1, 7)
        if not choice: break
        if not facade.visit_shop(choice, player): break
        facade.display_shop_menu(player)

def _handle_dungeon():
    if not player:
        print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)
        return
    
    # Ensure backward compatibility for save files that might lack current_depth
    if not hasattr(player, 'current_depth'):
        player.current_depth = 1
        
    print_header("🏰 DUNGEON MODE", "magenta")
    print(f"Current Depth: {player.current_depth}")
    
    if player.current_depth > 20:
        print(Fore.GREEN + "🎉 You have already conquered the dungeon!" + Style.RESET_ALL)
        return

    # COMPOSITION ROOT: Wire up dependencies
    presenter = ConsoleDungeonPresenter()
    spawner = GameSpawnStrategy()
    
    dungeon = Dungeon(
        spawner=spawner,
        presenter=presenter,
        depth=player.current_depth
    )
    
    success = dungeon.explore_from(player, battle)
    
    if success:
        if player.current_depth == 20:
            # Game complete
            player.current_depth += 1 # Mark as done
            # Optionally reset game or credits here
        else:
            player.current_depth += 1
            print(Fore.GREEN + f"💪 Depth increased! Next level: {player.current_depth}" + Style.RESET_ALL)
            # Autosave on floor completion
            save_game(player)
    else:
        # Player died or retreated
        if not player.is_alive():
            print(Fore.RED + "☠️ You died in the dungeon..." + Style.RESET_ALL)
            player.hp = player.max_hp
            # Depth does not increase on death

def _handle_role():
    # ... (Keep existing implementation) ...
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
    print("1) Warrior\n2) Mage\n3) Archer\n4) Healer\n5) Assassin\n6) Back")
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
        if not hasattr(player, 'current_depth'):
            player.current_depth = 1
        print(Fore.GREEN + f"✅ Welcome back, {player.name} (Depth: {player.current_depth})!")

def _handle_status():
    if player: display_status(player)
    else: print(Fore.RED + CONFIG.UI.MSG_CREATE_CHAR_FIRST)

# ==============================
# MAIN LOOP (Unchanged)
# ==============================

def game_loop():
    # ... (Keep existing implementation) ...
    handlers = {
        1: _handle_start_game, 2: _handle_status, 3: _handle_role,
        4: _handle_shop, 5: _handle_inventory_logic, 6: _handle_save,
        7: _handle_load, 8: _handle_dungeon,
    }
    
    while True:
        print_header("⚔️  WELCOME TO THE RPG ADVENTURE  ⚔️", "cyan")
        print("1. Start Game\n2. Show Status\n3. Choose Role\n4. Shop 🛒\n5. Inventory 🎒\n6. Save Game 💾\n7. Load Game 📂\n8. Dungeon 🏰\n9. Exit ❌")
        print_separator()
        choice = read_int("➤ Enter your choice: ", 1, 9)
        if choice == 9: 
            print(Fore.YELLOW + "\n🎮 Exiting game..." + Style.RESET_ALL)
            break
        if choice in handlers: handlers[choice]()
        else: print(CONFIG.UI.MSG_INVALID_CHOICE)

if __name__ == "__main__":
    show_loading_screen()
    game_loop()