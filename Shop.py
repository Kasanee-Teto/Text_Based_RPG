"""
Shop system for RPG Game
Manages item shops with categorized inventories
Easily extensible for new shop types and items
"""

from colorama import Fore, Style, init
from items import Weapon, Armor, Health_Potions
from typing import List, Optional

init(autoreset=True)


# ==============================
# BASE SHOP CLASS
# ==============================

class Shop:
    """
    Base shop class for managing item inventories
    
    Attributes:
        inventory_shop (List): Items available for purchase
        shop_name (str): Display name of the shop
    """
    
    def __init__(self, shop_name: str = "General Shop"):
        self.inventory_shop: List = []
        self.shop_name = shop_name
    
    def add_item(self, item):
        """
        Add a single item to shop inventory
        
        Args:
            item: Item object to add
        """
        self.inventory_shop.append(item)
    
    def stock_items(self, items: List):
        """
        Bulk add multiple items to shop
        
        Args:
            items: List of item objects
        """
        for item in items:
            self.add_item(item)
    
    def remove_item(self, item) -> bool:
        """
        Remove an item from shop (for limited stock)
        
        Args:
            item: Item to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if item in self.inventory_shop:
            self.inventory_shop. remove(item)
            return True
        return False
    
    def get_item_by_index(self, index: int) -> Optional[object]:
        """
        Get item by display index (1-based)
        
        Args:
            index: Display index
            
        Returns:
            Item if found, None otherwise
        """
        if 1 <= index <= len(self.inventory_shop):
            return self.inventory_shop[index - 1]
        return None
    
    def show_items(self, category_name: str = "Shop Inventory"):
        """
        Display all items with formatted output
        Shows stats, rarity, and pricing
        
        Args:
            category_name: Header title for the shop
        """
        if not self.inventory_shop:
            print(Fore.RED + "⚠️  No items available in this shop yet!" + Style.RESET_ALL)
            return
        
        print(Fore.YELLOW + f"\n{'=' * 50}" + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + f"{category_name. upper()}". center(50) + Style. RESET_ALL)
        print(Fore.YELLOW + f"{'=' * 50}" + Style.RESET_ALL)
        
        for i, item in enumerate(self.inventory_shop, 1):
            # Get rarity for color coding
            rarity = getattr(item, "rarity", "Common")
            color = self._get_rarity_color(rarity)
            
            # Dynamically detect item stats
            stats = self._get_item_stats(item)
            stat_text = " | ".join(stats) if stats else "No Bonus"
            
            # Display formatted item
            print(f"{i}. {color}{item.name}{Style.RESET_ALL} | {stat_text} | 💰 {item.value} | {color}{rarity}{Style.RESET_ALL}")
        
        print(Fore. YELLOW + "=" * 50 + "\n" + Style.RESET_ALL)
    
    def _get_rarity_color(self, rarity: str) -> str:
        """
        Get colorama color code for item rarity
        
        Args:
            rarity: Rarity tier string
            
        Returns:
            str: Colorama color code
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
        Extract stats from item dynamically
        
        Args:
            item: Item object
            
        Returns:
            List[str]: Formatted stat strings
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

class SwordShop(Shop):
    """
    Sword and melee weapon shop
    Stocks daggers, katanas, and great swords
    """
    
    def __init__(self):
        super().__init__("Sword Shop")
    
    def stock_sword_dagger(self):
        """Stock dagger category weapons"""
        self.stock_items([
            Weapon("Swiftfang", "Dagger", 12, 70, "Uncommon"),
            Weapon("Shadow Pierce", "Dagger", 20, 110, "Rare"),
            Weapon("Silent Fang", "Dagger", 17, 95, "Uncommon"),
            Weapon("Ironbite", "Dagger", 10, 55, "Common"),
            Weapon("Storm Edge", "Dagger", 25, 140, "Epic"),
        ])
    
    def stock_sword_katana(self):
        """Stock katana category weapons"""
        self.stock_items([
            Weapon("Kurohana", "Katana", 20, 100, "Uncommon"),
            Weapon("Tsukikage", "Katana", 30, 140, "Rare"),
            Weapon("Akatsuki Blade", "Katana", 35, 170, "Epic"),
            Weapon("Ryuuzan", "Katana", 18, 90, "Uncommon"),
            Weapon("Hikarimaru", "Katana", 28, 130, "Rare"),
        ])
    
    def stock_sword_great_sword(self):
        """Stock great sword category weapons"""
        self.stock_items([
            Weapon("Titanbreaker", "Great Sword", 22, 120, "Rare"),
            Weapon("Oblivion Fang", "Great Sword", 35, 170, "Epic"),
            Weapon("Dragon's Wrath", "Great Sword", 45, 210, "Legendary"),
            Weapon("Judgment Edge", "Great Sword", 18, 95, "Uncommon"),
            Weapon("Gravemourn", "Great Sword", 30, 150, "Rare"),
        ])
    
    def stock_all(self):
        """Stock all sword categories"""
        self.stock_sword_dagger()
        self. stock_sword_katana()
        self.stock_sword_great_sword()


class BowShop(Shop):
    """
    Ranged weapon shop
    Stocks various bow types
    """
    
    def __init__(self):
        super().__init__("Bow Shop")
    
    def stock_bows(self):
        """Stock all bow weapons"""
        self.stock_items([
            Weapon("Photon Arc", "Tech Bow", 28, 150, "Rare"),
            Weapon("Nova String", "Tech Bow", 35, 180, "Epic"),
            Weapon("Ionflare", "Tech Bow", 42, 220, "Legendary"),
            Weapon("Pulse Bow", "Tech Bow", 20, 120, "Uncommon"),
            Weapon("Plasma Piercer", "Tech Bow", 25, 140, "Rare"),
        ])


class GrimoireShop(Shop):
    """
    Magic grimoire shop
    Stocks spell books for mages
    """
    
    def __init__(self):
        super().__init__("Grimoire Shop")
    
    def stock_grimoires(self):
        """Stock all grimoire weapons"""
        self.stock_items([
            Weapon("Flame Codex", "Grimoire", 25, 120, "Rare"),
            Weapon("Aqua Tome", "Grimoire", 30, 140, "Rare"),
            Weapon("Terra Scroll", "Grimoire", 35, 160, "Epic"),
            Weapon("Tempest Grimoire", "Grimoire", 40, 180, "Epic"),
            Weapon("Infernal Codex", "Grimoire", 45, 200, "Legendary"),
        ])


class StaffShop(Shop):
    """
    Staff weapon shop
    Stocks staves for healers and support classes
    """
    
    def __init__(self):
        super().__init__("Staff Shop")
    
    def stock_staffs(self):
        """Stock all staff weapons"""
        self. stock_items([
            Weapon("Novice Staff", "Staff", 15, 80, "Common"),
            Weapon("Cleric Rod", "Staff", 20, 110, "Uncommon"),
            Weapon("Sanctum Wand", "Staff", 25, 140, "Rare"),
            Weapon("Seraph's Blessing", "Staff", 32, 180, "Epic"),
            Weapon("Divine Lumina", "Staff", 40, 220, "Legendary"),
        ])

    def stock_staffs(self):
        self.stock_items([
            Weapon("Novice Staff", "Staff", 15, 80),
            Weapon("Cleric Rod", "Staff", 20, 110),
            Weapon("Sanctum Wand", "Staff", 25, 140),
            Weapon("Seraph’s Blessing", "Staff", 32, 180),
            Weapon("Divine Lumina", "Staff", 40, 220),
        ])

class ArmorShop(Shop):
    """
    Armor and protection shop
    Stocks defensive equipment
    """
    
    def __init__(self):
        super().__init__("Armor Shop")
    
    def stock_armors(self):
        """Stock all armor pieces"""
        self.stock_items([
            Armor("Leather Vest", 8, "Light", 70, "Common"),
            Armor("Shadow Cloak", 12, "Light", 100, "Uncommon"),
            Armor("Wind Dancer Garb", 18, "Light", 130, "Rare"),
            Armor("Nightveil Shroud", 25, "Light", 180, "Epic"),
            Armor("Steel Plate Armor", 30, "Heavy", 200, "Rare"),
            Armor("Dragon Scale Mail", 40, "Heavy", 300, "Legendary"),
        ])


class PotionShop(Shop):
    """
    Consumable potion shop
    Stocks health restoration items
    """
    
    def __init__(self):
        super().__init__("Potion Shop")
    
    def stock_health_potions(self):
        """Stock all health potions"""
        self.stock_items([
            Health_Potions("Small Potion", 30, 25),
            Health_Potions("Medium Potion", 60, 50),
            Health_Potions("Large Potion", 100, 90),
            Health_Potions("Mega Potion", 150, 130),
            Health_Potions("Full Restore", 250, 999),  # Full heal
        ])


# ==============================
# LEGACY COMPATIBILITY
# ==============================

# Keep old class names for backward compatibility
shop_sword = SwordShop
shop_bow = BowShop
shop_grimoire = GrimoireShop
shop_staff = StaffShop
shop_armor = ArmorShop
shop_potion = PotionShop
