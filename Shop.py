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

init(autoreset=True)


# ==============================
# INTERFACES (ISP - Interface Segregation Principle)
# ==============================

class ShopInterface(Protocol):
    """
    Interface for shop operations.
    ISP: Small, focused interface with only essential shop methods.
    """
    def add_item(self, item: Any) -> None:
        """Add an item to the shop."""
        ...
    
    def get_items(self) -> List[Any]:
        """Get all items in the shop."""
        ...
    
    def get_item_count(self) -> int:
        """Get the number of items."""
        ...
    
    def get_shop_name(self) -> str:
        """Get the shop name."""
        ...


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
    
    Attributes:
        _inventory (List): Items available for purchase
        _shop_name (str): Display name of the shop
        _display_strategy (DisplayStrategy): How items are displayed
    """

    def __init__(
        self, 
        shop_name: str = "General Shop",
        display_strategy: Optional[DisplayStrategy] = None
    ):
        """
        Initialize a shop with dependency injection.
        
        Args:
            shop_name: Display name for the shop
            display_strategy: Strategy for displaying items (DIP)
        """
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
        
        Args:
            category_name: Optional custom header name
        
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

    def stock_sword_dagger(self) -> None:
        """Stock dagger category weapons."""
        self.stock_items([
            Weapon("Swiftfang", "Dagger", 12, 70),
            Weapon("Shadow Pierce", "Dagger", 20, 110),
            Weapon("Silent Fang", "Dagger", 17, 95),
            Weapon("Ironbite", "Dagger", 10, 55),
            Weapon("Storm Edge", "Dagger", 25, 140),
        ])

    def stock_sword_katana(self) -> None:
        """Stock katana category weapons."""
        self.stock_items([
            Weapon("Kurohana", "Katana", 20, 100),
            Weapon("Tsukikage", "Katana", 30, 140),
            Weapon("Akatsuki Blade", "Katana", 35, 170),
            Weapon("Ryuuzan", "Katana", 18, 90),
            Weapon("Hikarimaru", "Katana", 28, 130),
        ])

    def stock_sword_great_sword(self) -> None:
        """Stock great sword category weapons."""
        self.stock_items([
            Weapon("Titanbreaker", "Great Sword", 22, 120),
            Weapon("Oblivion Fang", "Great Sword", 35, 170),
            Weapon("Dragon's Wrath", "Great Sword", 45, 210),
            Weapon("Judgment Edge", "Great Sword", 18, 95),
            Weapon("Gravemourn", "Great Sword", 30, 150),
        ])

    def stock_all(self) -> None:
        """Stock all sword categories."""
        self.stock_sword_dagger()
        self.stock_sword_katana()
        self.stock_sword_great_sword()


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
    
    Manages shop type mappings and menu configuration.
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
    
    def get_all_shop_types(self) -> List[str]:
        """Get list of all available shop types."""
        return list(self._shop_configs.keys())
    
    def register_shop(
        self, 
        shop_type: str, 
        shop_class: type, 
        stock_methods: List[str], 
        display_name: str,
        menu_position: Optional[int] = None
    ) -> None:
        """
        Register a new shop type (OCP: extension without modification).
        
        Example:
            config.register_shop('jewelry', shop_jewelry, ['stock_rings'], '💍 Jewelry Shop', 7)
        """
        self._shop_configs[shop_type] = (shop_class, stock_methods, display_name)
        if menu_position:
            self._menu_mapping[menu_position] = shop_type


# ==============================
# PURCHASE SERVICE (SRP + DIP)
# ==============================

class PurchaseService:
    """
    SRP: Only responsible for coordinating purchase operations.
    DIP: Depends on abstractions (PurchaseValidator, TransactionProcessor).
    
    Coordinates validation and transaction processing.
    """
    
    def __init__(
        self,
        validator: Optional[PurchaseValidator] = None,
        processor: Optional[TransactionProcessor] = None
    ):
        """
        Initialize with dependency injection.
        
        Args:
            validator: Purchase validator (defaults to CoinPurchaseValidator)
            processor: Transaction processor (defaults to StandardTransactionProcessor)
        """
        self._validator = validator or CoinPurchaseValidator()
        self._processor = processor or StandardTransactionProcessor()
    
    def handle_purchase(self, shop: ShopInterface, player: Any) -> bool:
        """
        Coordinate the complete purchase flow.
        
        Args:
            shop: Shop to purchase from
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
        except (IndexError, AttributeError) as e:
            print(Fore.RED + f"❌ Error processing purchase: {e}" + Style.RESET_ALL)
            return True
    
    def _display_purchase_error(self, player: Any, item: Any, error_msg: str) -> None:
        """Display purchase error information."""
        price = getattr(item, "value", 0)
        shortage = price - player.coins
        
        print(Fore.RED + f"\n❌ {error_msg}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"💰 You have: {player.coins} coins" + Style.RESET_ALL)
        print(Fore.YELLOW + f"💵 You need: {price} coins" + Style.RESET_ALL)
        print(Fore.RED + f"📉 Short by: {shortage} coins" + Style.RESET_ALL)


# ==============================
# SHOP FACTORY (SRP + DIP)
# ==============================

class ShopFactory:
    """
    SRP: Only responsible for creating and initializing shop instances.
    DIP: Depends on ShopConfiguration abstraction.
    
    Factory pattern for shop creation.
    """
    
    def __init__(self, config: ShopConfiguration):
        """
        Initialize factory with configuration.
        
        Args:
            config: Shop configuration for creating shops
        """
        self._config = config
    
    def create_shop(
        self, 
        shop_type: str,
        display_strategy: Optional[DisplayStrategy] = None
    ) -> Optional[ShopInterface]:
        """
        Create and stock a shop instance.
        
        Args:
            shop_type: Type of shop to create
            display_strategy: Optional custom display strategy
            
        Returns:
            Fully stocked shop instance or None
        """
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
        shop_factory: Optional[ShopFactory] = None
    ):
        """
        Initialize facade with dependency injection.
        
        Args:
            config: Shop configuration (defaults to standard)
            purchase_service: Service for handling purchases
            shop_factory: Factory for creating shops
        """
        self._config = config or ShopConfiguration()
        self._purchase_service = purchase_service or PurchaseService()
        self._shop_factory = shop_factory or ShopFactory(self._config)
        self._current_shop: Optional[ShopInterface] = None
    
    def display_shop_menu(self, player: Any) -> None:
        """
        Display the main shop selection menu.
        
        Args:
            player: Player instance for displaying coins
        """
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + "🛒 WELCOME TO THE SHOP".center(60) + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print("1) ⚔️  Sword Shop     - Melee weapons (Daggers, Katanas, Great Swords)")
        print("2) 🛡️  Armor Shop     - Defensive equipment (Light & Heavy armor)")
        print("3) 🏹 Bow Shop       - Ranged weapons (Tech Bows)")
        print("4) 📜 Grimoire Shop  - Magic spell books (Elemental grimoires)")
        print("5) 💫 Staff Shop     - Support weapons (Healing staves)")
        print("6) 💊 Potion Shop    - Consumables (Health restoration)")
        print("7) 🚪 Exit Shop")
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
        print(Fore.GREEN + f"💰 Your Coins: {player.coins}" + Style.RESET_ALL)
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
    
    def visit_shop(self, shop_choice: int, player: Any) -> bool:
        # Exit option
        if shop_choice == 7:
            print(Fore.YELLOW + "👋 Thank you for visiting! Come again soon!" + Style.RESET_ALL)
            return False
        
        # Get shop type from menu choice
        shop_type = self._config.get_shop_type_by_menu(shop_choice)
        if not shop_type:
            print(Fore.RED + "❌ Invalid choice! Please select 1-7." + Style.RESET_ALL)
            return True
        
        # Handle the shop interaction
        return self._handle_shop_interaction(shop_type, player)
    
    def _handle_shop_interaction(self, shop_type: str, player: Any) -> bool:
        """
        Coordinate the complete shop interaction flow.
        
        Args:
            shop_type: Type of shop to visit
            player: Player instance
            
        Returns:
            True to continue shopping
        """
        # Create shop using factory
        self._current_shop = self._shop_factory.create_shop(shop_type)
        
        if not self._current_shop:
            print(Fore.RED + "❌ Shop not available!" + Style.RESET_ALL)
            return True
        
        # Display items
        self._current_shop.show_items()
        
        # Handle purchase using purchase service
        return self._purchase_service.handle_purchase(self._current_shop, player)
    
    def get_shop_by_type(self, shop_type: str) -> Optional[ShopInterface]:
        """
        Get a fully stocked shop instance by type.
        
        Args:
            shop_type: Type identifier ('sword', 'bow', etc.)
            
        Returns:
            Stocked shop instance or None
        """
        return self._shop_factory.create_shop(shop_type)


# ==============================
# CONVENIENCE FUNCTIONS (Factory Functions)
# ==============================

def create_shop_facade() -> ShopFacade:
    """
    Factory function to create a ShopFacade with default configuration.
    
    Returns:
        Configured ShopFacade instance with all dependencies
        
    Example:
        facade = create_shop_facade()
        facade.display_shop_menu(player)
    """
    config = ShopConfiguration()
    purchase_service = PurchaseService()
    shop_factory = ShopFactory(config)
    return ShopFacade(config, purchase_service, shop_factory)


def create_custom_shop_facade(
    config: Optional[ShopConfiguration] = None,
    display_strategy: Optional[DisplayStrategy] = None,
    validator: Optional[PurchaseValidator] = None,
    processor: Optional[TransactionProcessor] = None
) -> ShopFacade:
    """
    Factory function to create a fully customized ShopFacade.
    
    DIP: All dependencies can be injected for maximum flexibility.
    
    Args:
        config: Custom shop configuration
        display_strategy: Custom display strategy for all shops
        validator: Custom purchase validator
        processor: Custom transaction processor
    """
    shop_config = config or ShopConfiguration()
    purchase_service = PurchaseService(validator, processor)
    shop_factory = ShopFactory(shop_config)