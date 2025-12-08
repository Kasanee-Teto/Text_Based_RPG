# ==============================
# SHOP SYSTEM WITH FACADE PATTERN
# ==============================
"""
Shop system for RPG Game with Facade Pattern implementation. 
Manages multiple specialized shops with a unified interface. 

Design Patterns:
    - Facade Pattern: ShopFacade simplifies complex shop interactions
    - Factory Pattern: Dynamic shop creation and initialization
    - Template Method: Base Shop class with customizable stocking methods

Architecture:
    - Highly scalable: Easy to add new shop types
    - Maintainable: Clear separation of concerns
    - Type-safe: Full type hints for better IDE support
"""

from colorama import Fore, Style, init
from items import Weapon, Armor, Health_Potions
from typing import Optional, Dict, List, Tuple, Callable
from abc import ABC

init(autoreset=True)


# ==============================
# BASE SHOP CLASS
# ==============================
class Shop(ABC):
    """
    Base Shop class that manages item storage and display. 
    Each subclass implements specific item stocking methods.
    
    Attributes:
        inventory_shop (List): Items available for purchase
        shop_name (str): Display name of the shop
    
    Design: Template Method Pattern - subclasses customize stocking behavior
    """

    def __init__(self, shop_name: str = "General Shop"):
        """
        Initialize a shop with an empty inventory.
        
        Args:
            shop_name: Display name for the shop
        """
        self.inventory_shop: List = []
        self.shop_name = shop_name

    def add_item(self, item) -> None:
        """
        Add a single item to shop inventory.
        
        Args:
            item: Item object (Weapon, Armor, or Consumable)
        """
        self.inventory_shop.append(item)

    def stock_items(self, items: List) -> None:
        """
        Bulk add multiple items to shop inventory.
        
        Args:
            items: List of item objects to add
        """
        for item in items:
            self.add_item(item)

    def clear_inventory(self) -> None:
        """Remove all items from shop inventory."""
        self.inventory_shop.clear()

    def get_item_count(self) -> int:
        """
        Get the number of items in shop. 
        
        Returns:
            Number of items in inventory
        """
        return len(self.inventory_shop)

    def show_items(self, category_name: Optional[str] = None) -> None:
        """
        Display all items with formatted output including stats and rarity.
        
        Args:
            category_name: Optional custom header name (defaults to shop_name)
        
        Design: Dynamically detects and displays item attributes
        """
        display_name = category_name or self.shop_name
        
        if not self.inventory_shop:
            print(Fore.RED + "⚠️ No items available in this shop yet!" + Style.RESET_ALL)
            return

        # Header
        print(Fore. YELLOW + f"\n{'=' * 60}" + Style.RESET_ALL)
        print(Fore. CYAN + Style.BRIGHT + f"{display_name. upper()}". center(60) + Style. RESET_ALL)
        print(Fore.YELLOW + f"{'=' * 60}" + Style.RESET_ALL)
        
        # Item listing
        for i, item in enumerate(self. inventory_shop, 1):
            rarity = getattr(item, "rarity", "Common")
            color = self._get_rarity_color(rarity)
            stats = self._get_item_stats(item)
            stat_text = " | ".join(stats) if stats else "No Bonus"
            
            print(
                f"{i}. {color}{item.name}{Style. RESET_ALL} | "
                f"{stat_text} | 💰 {item.value} | "
                f"{color}[{rarity}]{Style.RESET_ALL}"
            )
        
        # Footer
        print(Fore.YELLOW + f"{'=' * 60}\n" + Style.RESET_ALL)

    def _get_rarity_color(self, rarity: str) -> str:
        """
        Get colorama color code for item rarity.
        
        Args:
            rarity: Rarity tier string
            
        Returns:
            Colorama color code
        """
        color_map = {
            "Common": Fore.WHITE,
            "Uncommon": Fore.GREEN,
            "Rare": Fore.BLUE,
            "Epic": Fore.MAGENTA,
            "Legendary": Fore.YELLOW,
        }
        return color_map. get(rarity, Fore. WHITE)

    def _get_item_stats(self, item) -> List[str]:
        """
        Extract and format stats from item dynamically.
        
        Args:
            item: Item object to analyze
            
        Returns:
            List of formatted stat strings
        """
        stats = []
        stat_attributes = {
            "damage": "Damage",
            "defense": "Defense",
            "heals": "Heals"
        }
        
        for attr, display_name in stat_attributes.items():
            if hasattr(item, attr):
                value = getattr(item, attr)
                stats.append(f"{display_name}: +{value}")
        
        return stats


# ==============================
# SPECIALIZED SHOP CLASSES
# ==============================

class shop_sword(Shop):
    """
    Sword and melee weapon shop.
    Offers daggers, katanas, and great swords with various rarities.
    """

    def __init__(self):
        super().__init__("⚔️ Sword Shop")

    def stock_sword_dagger(self) -> None:
        """Stock dagger category weapons - fast, low-medium damage."""
        self.stock_items([
            Weapon("Swiftfang", "Dagger", 12, 70),
            Weapon("Shadow Pierce", "Dagger", 20, 110),
            Weapon("Silent Fang", "Dagger", 17, 95),
            Weapon("Ironbite", "Dagger", 10, 55),
            Weapon("Storm Edge", "Dagger", 25, 140),
        ])

    def stock_sword_katana(self) -> None:
        """Stock katana category weapons - balanced damage and speed."""
        self.stock_items([
            Weapon("Kurohana", "Katana", 20, 100),
            Weapon("Tsukikage", "Katana", 30, 140),
            Weapon("Akatsuki Blade", "Katana", 35, 170),
            Weapon("Ryuuzan", "Katana", 18, 90),
            Weapon("Hikarimaru", "Katana", 28, 130),
        ])

    def stock_sword_great_sword(self) -> None:
        """Stock great sword category weapons - high damage, slower attacks."""
        self.stock_items([
            Weapon("Titanbreaker", "Great Sword", 22, 120),
            Weapon("Oblivion Fang", "Great Sword", 35, 170),
            Weapon("Dragon's Wrath", "Great Sword", 45, 210),
            Weapon("Judgment Edge", "Great Sword", 18, 95),
            Weapon("Gravemourn", "Great Sword", 30, 150),
        ])

    def stock_all(self) -> None:
        """Stock all sword categories - complete inventory."""
        self.stock_sword_dagger()
        self. stock_sword_katana()
        self.stock_sword_great_sword()


class shop_bow(Shop):
    """
    Ranged weapon shop specializing in bows and tech weapons.
    """

    def __init__(self):
        super().__init__("🏹 Bow Shop")

    def stock_bows(self) -> None:
        """Stock all bow types - ranged tech weapons."""
        self.stock_items([
            Weapon("Photon Arc", "Tech Bow", 28, 150),
            Weapon("Nova String", "Tech Bow", 35, 180),
            Weapon("Ionflare", "Tech Bow", 42, 220),
            Weapon("Pulse Bow", "Tech Bow", 20, 120),
            Weapon("Plasma Piercer", "Tech Bow", 25, 140),
        ])


class shop_grimoire(Shop):
    """
    Magic shop specializing in grimoires and spell books.
    Ideal for mage characters.
    """

    def __init__(self):
        super().__init__("📜 Grimoire Shop")

    def stock_grimoires(self) -> None:
        """Stock magical grimoires - elemental spell books."""
        self.stock_items([
            Weapon("Flame Codex", "Grimoire", 25, 120),
            Weapon("Aqua Tome", "Grimoire", 30, 140),
            Weapon("Terra Scroll", "Grimoire", 35, 160),
            Weapon("Tempest Grimoire", "Grimoire", 40, 180),
            Weapon("Infernal Codex", "Grimoire", 45, 200),
        ])


class shop_staff(Shop):
    """
    Staff weapon shop for healers and support classes.
    Offers healing-focused equipment.
    """

    def __init__(self):
        super().__init__("💫 Staff Shop")

    def stock_staffs(self) -> None:
        """Stock healing staves - support weapons."""
        self.stock_items([
            Weapon("Novice Staff", "Staff", 15, 80),
            Weapon("Cleric Rod", "Staff", 20, 110),
            Weapon("Sanctum Wand", "Staff", 25, 140),
            Weapon("Seraph's Blessing", "Staff", 32, 180),
            Weapon("Divine Lumina", "Staff", 40, 220),
        ])


class shop_armor(Shop):
    """
    Armor shop for defensive equipment.
    Offers protection gear of various types.
    """

    def __init__(self):
        super().__init__("🛡️ Armor Shop")

    def stock_armors(self) -> None:
        """Stock defensive armor - light and heavy types."""
        self.stock_items([
            Armor("Leather Vest", 8, "Light", 70),
            Armor("Shadow Cloak", 12, "Light", 100),
            Armor("Wind Dancer Garb", 18, "Light", 130),
            Armor("Nightveil Shroud", 25, "Light", 180),
        ])


class shop_potion(Shop):
    """
    Consumables shop specializing in healing potions.
    Essential for sustaining through difficult battles.
    """

    def __init__(self):
        super().__init__("💊 Potion Shop")

    def stock_health_potions(self) -> None:
        """Stock health restoration potions - various sizes."""
        self.stock_items([
            Health_Potions("Small Potion", 25, 30),
            Health_Potions("Medium Potion", 50, 60),
            Health_Potions("Large Potion", 90, 100),
            Health_Potions("Mega Potion", 130, 150),
        ])


# ==============================
# SHOP CONFIGURATION
# ==============================

class ShopConfiguration:
    """
    Configuration class for shop types and their initialization.
    Makes it easy to add new shops without modifying core facade logic.
    
    Design: Configuration object separates data from behavior
    """
    
    def __init__(self):
        """Initialize shop configuration mappings."""
        self._shop_configs: Dict[str, Tuple[type, List[str], str]] = {
            'sword': (shop_sword, ['stock_all'], "⚔️ Sword Shop"),
            'bow': (shop_bow, ['stock_bows'], "🏹 Bow Shop"),
            'grimoire': (shop_grimoire, ['stock_grimoires'], "📜 Grimoire Shop"),
            'staff': (shop_staff, ['stock_staffs'], "💫 Staff Shop"),
            'armor': (shop_armor, ['stock_armors'], "🛡️ Armor Shop"),
            'potion': (shop_potion, ['stock_health_potions'], "💊 Potion Shop")
        }
        
        self._menu_mapping: Dict[int, str] = {
            1: 'sword',
            2: 'armor',
            3: 'bow',
            4: 'grimoire',
            5: 'staff',
            6: 'potion'
        }
    
    def get_shop_config(self, shop_type: str) -> Optional[Tuple[type, List[str], str]]:
        """
        Get configuration for a specific shop type.
        
        Args:
            shop_type: Type identifier ('sword', 'bow', etc.)
            
        Returns:
            Tuple of (ShopClass, stock_methods, display_name) or None
        """
        return self._shop_configs.get(shop_type)
    
    def get_shop_type_by_menu(self, menu_choice: int) -> Optional[str]:
        """
        Map menu number to shop type.
        
        Args:
            menu_choice: Menu option number (1-6)
            
        Returns:
            Shop type string or None
        """
        return self._menu_mapping.get(menu_choice)
    
    def get_all_shop_types(self) -> List[str]:
        """
        Get list of all available shop types.
        
        Returns:
            List of shop type identifiers
        """
        return list(self._shop_configs.keys())
    
    def register_shop(self, 
                     shop_type: str, 
                     shop_class: type, 
                     stock_methods: List[str], 
                     display_name: str,
                     menu_position: Optional[int] = None) -> None:
        """
        Register a new shop type (for extensibility).
        
        Args:
            shop_type: Unique identifier for the shop
            shop_class: Shop class to instantiate
            stock_methods: Methods to call for stocking
            display_name: Display name for UI
            menu_position: Optional menu position
        
        Example:
            config. register_shop('jewelry', shop_jewelry, ['stock_rings'], '💍 Jewelry Shop', 7)
        """
        self._shop_configs[shop_type] = (shop_class, stock_methods, display_name)
        if menu_position:
            self._menu_mapping[menu_position] = shop_type


# ==============================
# FACADE PATTERN - SHOP FACADE
# ==============================

class ShopFacade:
    """
    Facade Pattern: Unified interface for all shop operations.
    
    Benefits:
        - Simplifies complex shop interactions
        - Hides internal shop management from client code
        - Provides single entry point for all shop operations
        - Makes adding new shops trivial
    
    Design Principles:
        - Single Responsibility: Only handles shop coordination
        - Open/Closed: Open for extension via ShopConfiguration
        - Dependency Inversion: Depends on Shop abstraction
    """
    
    def __init__(self, config: Optional[ShopConfiguration] = None):
        """
        Initialize the shop facade.
        
        Args:
            config: Optional custom shop configuration (defaults to standard)
        """
        self._config = config or ShopConfiguration()
        self._current_shop: Optional[Shop] = None
    
    def display_shop_menu(self, player) -> None:
        """
        Display the main shop selection menu with player info.
        
        Args:
            player: Player instance for displaying coins
        """
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print(Fore. CYAN + Style.BRIGHT + "🛒 WELCOME TO THE SHOP". center(60) + Style. RESET_ALL)
        print(Fore.YELLOW + "=" * 60 + Style. RESET_ALL)
        print("1) ⚔️  Sword Shop     - Melee weapons (Daggers, Katanas, Great Swords)")
        print("2) 🛡️  Armor Shop     - Defensive equipment (Light & Heavy armor)")
        print("3) 🏹 Bow Shop       - Ranged weapons (Tech Bows)")
        print("4) 📜 Grimoire Shop  - Magic spell books (Elemental grimoires)")
        print("5) 💫 Staff Shop     - Support weapons (Healing staves)")
        print("6) 💊 Potion Shop    - Consumables (Health restoration)")
        print("7) 🚪 Exit Shop")
        print(Fore.YELLOW + "-" * 60 + Style. RESET_ALL)
        print(Fore.GREEN + f"💰 Your Coins: {player.coins}" + Style.RESET_ALL)
        print(Fore. YELLOW + "-" * 60 + Style.RESET_ALL)
    
    def visit_shop(self, shop_choice: int, player) -> bool:
        """
        Handle a shop visit based on player's menu choice.
        
        Args:
            shop_choice: Menu number (1-7)
            player: Player instance
            
        Returns:
            True if continuing shopping, False if exiting
        """
        # Exit option
        if shop_choice == 7:
            print(Fore. YELLOW + "👋 Thank you for visiting!  Come again soon!" + Style.RESET_ALL)
            return False
        
        # Get shop type from menu choice
        shop_type = self._config.get_shop_type_by_menu(shop_choice)
        if not shop_type:
            print(Fore.RED + "❌ Invalid choice! Please select 1-7." + Style. RESET_ALL)
            return True
        
        # Handle the shop interaction
        return self._handle_shop_interaction(shop_type, player)
    
    def _handle_shop_interaction(self, shop_type: str, player) -> bool:
        """
        Coordinate the complete shop interaction flow.
        
        Args:
            shop_type: Type of shop ('sword', 'bow', etc.)
            player: Player instance
            
        Returns:
            True to continue shopping
            
        Design: Template Method - defines skeleton of shop visit
        """
        # Get shop configuration
        shop_config = self._config.get_shop_config(shop_type)
        if not shop_config:
            print(Fore. RED + "❌ Shop not available!" + Style.RESET_ALL)
            return True
        
        shop_class, stock_methods, shop_title = shop_config
        
        # Create and initialize shop
        self._current_shop = self._create_and_stock_shop(shop_class, stock_methods)
        
        # Display items
        self._current_shop.show_items(shop_title)
        
        # Handle purchase
        return self._process_purchase(self._current_shop, player)
    
    def _create_and_stock_shop(self, 
                               shop_class: type, 
                               stock_methods: List[str]) -> Shop:
        """
        Factory method to create and stock a shop instance.
        
        Args:
            shop_class: Shop class to instantiate
            stock_methods: Methods to call for stocking
            
        Returns:
            Fully stocked shop instance
        """
        shop = shop_class()
        for method_name in stock_methods:
            if hasattr(shop, method_name):
                getattr(shop, method_name)()
        return shop
    
    def _process_purchase(self, shop: Shop, player) -> bool:
        """
        Handle the purchase transaction with validation and feedback.
        
        Args:
            shop: Shop instance to purchase from
            player: Player making the purchase
            
        Returns:
            True to continue shopping
        """
        try:
            choice_prompt = (
                f"{Fore.CYAN}➤ Select item number to buy "
                f"(0 to return): {Style.RESET_ALL}"
            )
            buy_choice = int(input(choice_prompt))
            
            # Cancel purchase
            if buy_choice == 0:
                print(Fore. YELLOW + "↩️  Returning to shop menu..." + Style.RESET_ALL)
                return True
            
            # Validate selection range
            if not (1 <= buy_choice <= shop.get_item_count()):
                print(Fore.RED + 
                      f"❌ Invalid selection! Choose 1-{shop.get_item_count()}" + 
                      Style.RESET_ALL)
                return True
            
            # Get selected item
            selected_item = shop.inventory_shop[buy_choice - 1]
            price = getattr(selected_item, "value", 0)
            item_name = getattr(selected_item, "name", "Unknown Item")
            
            # Check affordability and complete purchase
            if player.coins >= price:
                return self._complete_purchase(player, selected_item, price, item_name)
            else:
                return self._handle_insufficient_funds(player, price)
            
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter a number." + Style.RESET_ALL)
            return True
        except (IndexError, AttributeError) as e:
            print(Fore.RED + f"❌ Error processing purchase: {e}" + Style. RESET_ALL)
            return True
    
    def _complete_purchase(self, 
                          player, 
                          item, 
                          price: int, 
                          item_name: str) -> bool:
        """
        Complete a successful purchase transaction.
        
        Args:
            player: Player making purchase
            item: Item being purchased
            price: Cost of item
            item_name: Name of item for display
            
        Returns:
            True to continue shopping
        """
        player.coins -= price
        player.inventory. add_item(item)
        
        print(Fore.GREEN + f"\n✅ Purchase successful!" + Style.RESET_ALL)
        print(Fore.WHITE + f"📦 You bought: {item_name}" + Style.RESET_ALL)
        print(Fore. YELLOW + f"💰 Coins remaining: {player.coins}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📝 Item added to inventory!" + Style.RESET_ALL)
        
        return True
    
    def _handle_insufficient_funds(self, player, price: int) -> bool:
        """
        Handle case where player cannot afford item.
        
        Args:
            player: Player attempting purchase
            price: Cost of desired item
            
        Returns:
            True to continue shopping
        """
        shortage = price - player.coins
        print(Fore.RED + f"\n❌ Insufficient funds!" + Style.RESET_ALL)
        print(Fore. YELLOW + f"💰 You have: {player.coins} coins" + Style.RESET_ALL)
        print(Fore.YELLOW + f"💵 You need: {price} coins" + Style.RESET_ALL)
        print(Fore.RED + f"📉 Short by: {shortage} coins" + Style.RESET_ALL)
        
        return True
    
    def get_shop_by_type(self, shop_type: str) -> Optional[Shop]:
        """
        Get a fully stocked shop instance by type.
        Useful for testing or advanced features.
        
        Args:
            shop_type: Type identifier ('sword', 'bow', etc.)
            
        Returns:
            Stocked shop instance or None
            
        Example:
            sword_shop = facade.get_shop_by_type('sword')
        """
        shop_config = self._config.get_shop_config(shop_type)
        if shop_config:
            shop_class, stock_methods, _ = shop_config
            return self._create_and_stock_shop(shop_class, stock_methods)
        return None


# ==============================
# CONVENIENCE FUNCTIONS
# ==============================

def create_shop_facade() -> ShopFacade:
    """
    Factory function to create a ShopFacade with default configuration.
    
    Returns:
        Configured ShopFacade instance
        
    Example:
        facade = create_shop_facade()
        facade.display_shop_menu(player)
    """
    return ShopFacade()


def create_custom_shop_facade(config: ShopConfiguration) -> ShopFacade:
    """
    Factory function to create a ShopFacade with custom configuration.
    
    Args:
        config: Custom shop configuration
        
    Returns:
        Configured ShopFacade instance
    """
    return ShopFacade(config)