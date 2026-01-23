"""
Shop system for RPG Game with SOLID Principles implementation. 
Manages multiple specialized shops with a unified interface. 

SOLID Principles Applied:
    1. Single Responsibility Principle (SRP):
       - Each class has one reason to change
       - ItemDisplayer: Only handles item display
       - PurchaseProcessor: Only handles purchase logic
       - Shop classes: Only manage inventory
       
    2. Open/Closed Principle (OCP):
       - Open for extension via inheritance and interfaces
       - Closed for modification via abstractions
       - New shop types can be added without modifying existing code
       
    3. Liskov Substitution Principle (LSP):
       - All Shop subclasses can replace base Shop class
       - ShopInterface ensures contract compliance
       
    4. Interface Segregation Principle (ISP):
       - Focused interfaces (ShopInterface, DisplayStrategy, etc.)
       - Classes only depend on methods they use
       
    5. Dependency Inversion Principle (DIP):
       - Depend on abstractions (interfaces/abstract classes)
       - High-level modules (ShopFacade) don't depend on low-level modules

Design Patterns:
    - Facade Pattern: ShopFacade simplifies complex shop interactions
    - Strategy Pattern: Different display and pricing strategies
    - Factory Pattern: Dynamic shop creation and initialization
    - Dependency Injection: Dependencies injected via constructors
"""

from colorama import Fore, Style, init
from items import Weapon, Armor, HealthPotion
from typing import Optional, Dict, List, Tuple, Protocol, Any
from abc import ABC, abstractmethod
from config import CONFIG 

init(autoreset=True)


# ==============================
# INTERFACES (ISP - Interface Segregation Principle)
# ==============================

class ShopInterface(Protocol):
    """
    Interface for shop operations.
    ISP: Small, focused interface with only essential shop methods.
    """
    def add_item(self, item: Any) -> None: ...
    def get_items(self) -> List[Any]: ...
    def get_item_count(self) -> int: ...
    def get_shop_name(self) -> str: ...


class DisplayStrategy(ABC):
    """
    SRP: Responsible only for displaying items.
    OCP: Can be extended with new display strategies without modifying existing code.
    """
    @abstractmethod
    def display(self, items: List[Any], shop_name: str) -> None:
        """Display items in a specific format."""
        pass


class PurchaseValidator(ABC):
    """
    SRP: Responsible only for validating purchases.
    OCP: Can be extended with new validation rules.
    """
    @abstractmethod
    def can_purchase(self, player: Any, item: Any) -> Tuple[bool, str]:
        """
        Validate if purchase can proceed.
        Returns: (is_valid, error_message)
        """
        pass


class TransactionProcessor(ABC):
    """
    SRP: Responsible only for processing transactions.
    DIP: Depends on abstractions, not concrete implementations.
    """
    @abstractmethod
    def process(self, player: Any, item: Any, price: int) -> bool:
        """Process a purchase transaction."""
        pass


# ==============================
# CONCRETE IMPLEMENTATIONS (SRP)
# ==============================

class StandardDisplayStrategy(DisplayStrategy):
    """
    SRP: Only responsible for standard item display formatting.
    Handles the visual presentation of shop items.
    """
    
    def display(self, items: List[Any], shop_name: str) -> None:
        """Display items in standard format with colors and stats."""
        if not items:
            print(Fore.RED + "⚠️ No items available in this shop yet!" + Style.RESET_ALL)
            return

        # Header
        print(Fore.YELLOW + f"\n{'=' * 60}" + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + f"{shop_name.upper()}".center(60) + Style.RESET_ALL)
        print(Fore.YELLOW + f"{'=' * 60}" + Style.RESET_ALL)
        
        # Item listing
        for i, item in enumerate(items, 1):
            rarity = getattr(item, "rarity", "Common")
            color = self._get_rarity_color(rarity)
            stats = self._get_item_stats(item)
            stat_text = " | ".join(stats) if stats else "No Bonus"
            
            print(
                f"{i}. {color}{item.name}{Style.RESET_ALL} | "
                f"{stat_text} | 💰 {item.value} | "
                f"{color}[{rarity}]{Style.RESET_ALL}"
            )
        
        # Footer
        print(Fore.YELLOW + f"{'=' * 60}\n" + Style.RESET_ALL)
    
    def _get_rarity_color(self, rarity: str) -> str:
        """Get color code for item rarity."""
        color_map = {
            "Common": Fore.WHITE,
            "Uncommon": Fore.GREEN,
            "Rare": Fore.BLUE,
            "Epic": Fore.MAGENTA,
            "Legendary": Fore.YELLOW,
        }
        return color_map.get(rarity, Fore.WHITE)
    
    def _get_item_stats(self, item: Any) -> List[str]:
        """Extract and format stats from item."""
        stats = []
        if hasattr(item, "damage"):
            stats.append(f"Damage: +{item.damage}")
        if hasattr(item, "defense"):
            stats.append(f"Defense: +{item.defense}")
        return stats


class CoinPurchaseValidator(PurchaseValidator):
    """
    SRP: Only responsible for validating coin-based purchases.
    Can be extended for different validation rules.
    """
    
    def can_purchase(self, player: Any, item: Any) -> Tuple[bool, str]:
        """Check if player has enough coins."""
        price = getattr(item, "value", 0)
        if player.coins >= price:
            return True, ""
        else:
            shortage = price - player.coins
            return False, f"Insufficient funds! Need {shortage} more coins."


class StandardTransactionProcessor(TransactionProcessor):
    """
    SRP: Only responsible for processing standard purchase transactions.
    Handles coin deduction and inventory updates.
    """
    
    def process(self, player: Any, item: Any, price: int) -> bool:
        """Execute the purchase transaction."""
        try:
            player.coins -= price
            player.inventory.add_item(item)
            
            print(Fore.GREEN + f"\n✅ Purchase successful!" + Style.RESET_ALL)
            print(Fore.WHITE + f"📦 You bought: {item.name}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"💰 Coins remaining: {player.coins}" + Style.RESET_ALL)
            print(Fore.CYAN + f"📝 Item added to inventory!" + Style.RESET_ALL)
            
            return True
        except Exception as e:
            print(Fore.RED + f"❌ Transaction failed: {e}" + Style.RESET_ALL)
            return False


# ==============================
# BASE SHOP CLASS (SRP + LSP + DIP)
# ==============================

class Shop(ABC):
    """
    Base Shop class following SOLID principles.
    
    SRP: Only manages inventory, delegates display and transactions.
    LSP: All subclasses can substitute this base class.
    DIP: Depends on abstractions (DisplayStrategy, not concrete implementations).
    """

    def __init__(
        self, 
        shop_name: str = "General Shop",
        display_strategy: Optional[DisplayStrategy] = None
    ):
        self._inventory: List[Any] = []
        self._shop_name = shop_name
        # DIP: Depend on abstraction, with default concrete implementation
        self._display_strategy = display_strategy or StandardDisplayStrategy()

    def add_item(self, item: Any) -> None:
        """Add a single item to shop inventory."""
        self._inventory.append(item)

    def stock_items(self, items: List[Any]) -> None:
        """Bulk add multiple items to shop inventory."""
        for item in items:
            self.add_item(item)

    def clear_inventory(self) -> None:
        """Remove all items from shop inventory."""
        self._inventory.clear()

    def get_item_count(self) -> int:
        """Get the number of items in shop."""
        return len(self._inventory)
    
    def get_items(self) -> List[Any]:
        """Get all items in the shop."""
        return self._inventory.copy()
    
    def get_shop_name(self) -> str:
        """Get the shop name."""
        return self._shop_name

    def show_items(self, category_name: Optional[str] = None) -> None:
        """
        Display all items using the injected display strategy.
        SRP: Delegates display logic to DisplayStrategy
        """
        display_name = category_name or self._shop_name
        self._display_strategy.display(self._inventory, display_name)


# ==============================
# SPECIALIZED SHOP CLASSES (LSP + OCP)
# ==============================

class shop_sword(Shop):
    """
    Sword and melee weapon shop.
    LSP: Can substitute Shop base class.
    OCP: Extends Shop without modifying it.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("⚔️ Sword Shop", display_strategy)

    def stock_all(self) -> None:
        """Stock all sword categories."""
        self.stock_items([
            Weapon("Swiftfang", "Dagger", 12, 70),
            Weapon("Shadow Pierce", "Dagger", 20, 110),
            Weapon("Silent Fang", "Dagger", 17, 95),
            Weapon("Ironbite", "Dagger", 10, 55),
            Weapon("Storm Edge", "Dagger", 25, 140),
            Weapon("Kurohana", "Katana", 20, 100),
            Weapon("Tsukikage", "Katana", 30, 140),
            Weapon("Akatsuki Blade", "Katana", 35, 170),
            Weapon("Ryuuzan", "Katana", 18, 90),
            Weapon("Hikarimaru", "Katana", 28, 130),
            Weapon("Titanbreaker", "Great Sword", 22, 120),
            Weapon("Oblivion Fang", "Great Sword", 35, 170),
            Weapon("Dragon's Wrath", "Great Sword", 45, 210),
            Weapon("Judgment Edge", "Great Sword", 18, 95),
            Weapon("Gravemourn", "Great Sword", 30, 150),
        ])


class shop_bow(Shop):
    """
    Ranged weapon shop specializing in bows.
    LSP: Can substitute Shop base class.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("🏹 Bow Shop", display_strategy)

    def stock_bows(self) -> None:
        """Stock all bow types."""
        self.stock_items([
            Weapon("Photon Arc", "Tech Bow", 28, 150),
            Weapon("Nova String", "Tech Bow", 35, 180),
            Weapon("Ionflare", "Tech Bow", 42, 220),
            Weapon("Pulse Bow", "Tech Bow", 20, 120),
            Weapon("Plasma Piercer", "Tech Bow", 25, 140),
        ])


class shop_grimoire(Shop):
    """
    Magic shop specializing in grimoires.
    LSP: Can substitute Shop base class completely.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("📜 Grimoire Shop", display_strategy)

    def stock_grimoires(self) -> None:
        """Stock magical grimoires."""
        self.stock_items([
            Weapon("Flame Codex", "Grimoire", 25, 120),
            Weapon("Aqua Tome", "Grimoire", 30, 140),
            Weapon("Terra Scroll", "Grimoire", 35, 160),
            Weapon("Tempest Grimoire", "Grimoire", 40, 180),
            Weapon("Infernal Codex", "Grimoire", 45, 200),
        ])


class shop_staff(Shop):
    """
    Staff weapon shop for healers.
    LSP: Can substitute Shop base class completely.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("💫 Staff Shop", display_strategy)

    def stock_staffs(self) -> None:
        """Stock healing staves."""
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
    LSP: Can substitute Shop base class completely.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("🛡️ Armor Shop", display_strategy)

    def stock_armors(self) -> None:
        """Stock defensive armor."""
        self.stock_items([
            Armor("Leather Vest", 8, "Light", 70),
            Armor("Shadow Cloak", 12, "Light", 100),
            Armor("Wind Dancer Garb", 18, "Light", 130),
            Armor("Nightveil Shroud", 25, "Light", 180),
        ])


class shop_potion(Shop):
    """
    Consumables shop specializing in potions.
    LSP: Can substitute Shop base class completely.
    """

    def __init__(self, display_strategy: Optional[DisplayStrategy] = None):
        super().__init__("💊 Potion Shop", display_strategy)

    def stock_health_potions(self) -> None:
        """Stock health restoration potions."""
        self.stock_items([
            HealthPotion("Small Potion", 25, 30),
            HealthPotion("Medium Potion", 50, 60),
            HealthPotion("Large Potion", 90, 100),
            HealthPotion("Mega Potion", 130, 150),
        ])


# ==============================
# SHOP CONFIGURATION (SRP + OCP)
# ==============================

class ShopConfiguration:
    """
    SRP: Only responsible for shop configuration management.
    OCP: Open for extension - new shops can be registered without modification.
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
        """Get configuration for a specific shop type."""
        return self._shop_configs.get(shop_type)
    
    def get_shop_type_by_menu(self, menu_choice: int) -> Optional[str]:
        """Map menu number to shop type."""
        return self._menu_mapping.get(menu_choice)


# ==============================
# SERVICES (SRP + DIP)
# ==============================

class PurchaseService:
    """
    SRP: Only responsible for coordinating purchase operations.
    DIP: Depends on abstractions (PurchaseValidator, TransactionProcessor).
    """
    
    def __init__(
        self,
        validator: Optional[PurchaseValidator] = None,
        processor: Optional[TransactionProcessor] = None
    ):
        self._validator = validator or CoinPurchaseValidator()
        self._processor = processor or StandardTransactionProcessor()
    
    def handle_purchase(self, shop: ShopInterface, player: Any) -> bool:
        """Coordinate the complete purchase flow."""
        try:
            print(Fore.CYAN + "Enter 0 to return to menu." + Style.RESET_ALL)
            choice_prompt = (
                f"{Fore.CYAN}➤ Select item number to buy: {Style.RESET_ALL}"
            )
            buy_choice = int(input(choice_prompt))
            
            # Cancel purchase
            if buy_choice == 0:
                print(Fore.YELLOW + "↩️  Returning to shop menu..." + Style.RESET_ALL)
                return True
            
            # Validate selection range
            if not (1 <= buy_choice <= shop.get_item_count()):
                print(Fore.RED + 
                      f"❌ Invalid selection! Choose 1-{shop.get_item_count()}" + 
                      Style.RESET_ALL)
                return True
            
            # Get selected item
            items = shop.get_items()
            selected_item = items[buy_choice - 1]
            
            # Validate purchase
            can_buy, error_msg = self._validator.can_purchase(player, selected_item)
            if not can_buy:
                self._display_purchase_error(player, selected_item, error_msg)
                return True
            
            # Process transaction
            price = getattr(selected_item, "value", 0)
            return self._processor.process(player, selected_item, price)
            
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter a number." + Style.RESET_ALL)
            return True
    
    def _display_purchase_error(self, player: Any, item: Any, error_msg: str) -> None:
        """Display purchase error information."""
        price = getattr(item, "value", 0)
        shortage = price - player.coins
        
        print(Fore.RED + f"\n❌ {error_msg}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"💰 You have: {player.coins} coins" + Style.RESET_ALL)
        print(Fore.YELLOW + f"💵 You need: {price} coins" + Style.RESET_ALL)
        print(Fore.RED + f"📉 Short by: {shortage} coins" + Style.RESET_ALL)


class SalesService:
    """
    SRP: Responsible for handling item sales logic.
    Separated from PurchaseService to adhere to Single Responsibility Principle.
    """
    def handle_sale(self, player: Any) -> bool:
        """
        Manage the selling process loop.
        Returns: True to return to shop menu, False if exit requested (though usually returns True).
        """
        while True:
            items = player.inventory.items
            if not items:
                print(Fore.YELLOW + "\n📦 Your inventory is empty! Nothing to sell." + Style.RESET_ALL)
                return True

            print(Fore.YELLOW + f"\n{'=' * 60}" + Style.RESET_ALL)
            print(Fore.CYAN + Style.BRIGHT + "💰 SELL ITEMS".center(60) + Style.RESET_ALL)
            print(Fore.YELLOW + f"{'=' * 60}" + Style.RESET_ALL)
            print(Fore.WHITE + f"Current Coins: {player.coins}" + Style.RESET_ALL)
            print("-" * 60)

            # List items with calculated sell prices
            for i, item in enumerate(items, 1):
                sell_price = int(item.value * CONFIG.SELL_PRICE_MULTIPLIER)
                print(f"{i}. {item.name} | Value: {item.value} -> Sell Price: {Fore.GREEN}{sell_price}{Style.RESET_ALL}")
            
            print("-" * 60)
            print(Fore.CYAN + "Enter 0 to return to shop menu." + Style.RESET_ALL)
            
            try:
                choice = int(input("➤ Select item number to sell: "))
                if choice == 0: return True
                
                if 1 <= choice <= len(items):
                    item = items[choice - 1]
                    sell_price = int(item.value * CONFIG.SELL_PRICE_MULTIPLIER)
                    
                    player.coins += sell_price
                    player.inventory.remove_item(item)
                    
                    print(Fore.GREEN + f"\n✅ Sold {item.name} for {sell_price} coins!" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"💰 New Balance: {player.coins}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "❌ Invalid selection!" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "❌ Invalid input!" + Style.RESET_ALL)


# ==============================
# SHOP FACTORY (SRP + DIP)
# ==============================

class ShopFactory:
    """
    SRP: Only responsible for creating and initializing shop instances.
    DIP: Depends on ShopConfiguration abstraction.
    """
    
    def __init__(self, config: ShopConfiguration):
        self._config = config
    
    def create_shop(
        self, 
        shop_type: str,
        display_strategy: Optional[DisplayStrategy] = None
    ) -> Optional[ShopInterface]:
        """Create and stock a shop instance."""
        shop_config = self._config.get_shop_config(shop_type)
        if not shop_config:
            return None
        
        shop_class, stock_methods, _ = shop_config
        
        # Create shop with dependency injection
        shop = shop_class(display_strategy)
        
        # Stock the shop
        for method_name in stock_methods:
            if hasattr(shop, method_name):
                getattr(shop, method_name)()
        
        return shop


# ==============================
# FACADE PATTERN (SRP + DIP)
# ==============================

class ShopFacade:
    def __init__(
        self,
        config: Optional[ShopConfiguration] = None,
        purchase_service: Optional[PurchaseService] = None,
        sales_service: Optional[SalesService] = None,
        shop_factory: Optional[ShopFactory] = None
    ):
        """
        Initialize facade with dependency injection.
        Added SalesService dependency.
        """
        self._config = config or ShopConfiguration()
        self._purchase_service = purchase_service or PurchaseService()
        self._sales_service = sales_service or SalesService()
        self._shop_factory = shop_factory or ShopFactory(self._config)
        self._current_shop: Optional[ShopInterface] = None
    
    def display_shop_menu(self, player: Any) -> None:
        """Display the main shop selection menu."""
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + "🛒 WELCOME TO THE SHOP".center(60) + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print("1) ⚔️  Sword Shop     - Melee weapons")
        print("2) 🛡️  Armor Shop     - Defensive equipment")
        print("3) 🏹 Bow Shop       - Ranged weapons")
        print("4) 📜 Grimoire Shop  - Magic spell books")
        print("5) 💫 Staff Shop     - Support weapons")
        print("6) 💊 Potion Shop    - Consumables")
        print("7) 💰 Sell Items     - Convert items to coins")  # New Option
        print("8) 🚪 Exit Shop")
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
        print(Fore.GREEN + f"💰 Your Coins: {player.coins}" + Style.RESET_ALL)
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
    
    def visit_shop(self, shop_choice: int, player: Any) -> bool:
        # Exit option
        if shop_choice == 8:
            print(Fore.YELLOW + "👋 Thank you for visiting! Come again soon!" + Style.RESET_ALL)
            return False
        
        # Handle Sell Option
        if shop_choice == 7:
            return self._sales_service.handle_sale(player)
        
        # Get shop type from menu choice
        shop_type = self._config.get_shop_type_by_menu(shop_choice)
        if not shop_type:
            print(Fore.RED + "❌ Invalid choice! Please select 1-8." + Style.RESET_ALL)
            return True
        
        # Handle the shop interaction
        return self._handle_shop_interaction(shop_type, player)
    
    def _handle_shop_interaction(self, shop_type: str, player: Any) -> bool:
        """Coordinate the complete shop interaction flow."""
        # Create shop using factory
        self._current_shop = self._shop_factory.create_shop(shop_type)
        
        if not self._current_shop:
            print(Fore.RED + "❌ Shop not available!" + Style.RESET_ALL)
            return True
        
        # Display items
        self._current_shop.show_items()
        
        # Handle purchase using purchase service
        return self._purchase_service.handle_purchase(self._current_shop, player)