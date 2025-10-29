# ==============================
# 🏪 SHOP SYSTEM (OBJECT-BASED)
# ==============================

from colorama import Fore, Style, init
from items import Weapon, Armor, Health_Potions

init(autoreset=True)


class Shop:
    """
    Base Shop class that manages item storage and display.
    Each subclass stocks relevant object types.
    """

    def __init__(self):
        self.inventory_shop = []  # semua item tersimpan di sini

    def add_item(self, item):
        """Add an item (Weapon, Armor, Potion, etc.) to shop."""
        self.inventory_shop.append(item)

    def stock_items(self, items):
        """Bulk add items to shop inventory."""
        for item in items:
            self.add_item(item)

    def show_items(self, category_name="Shop Inventory"):
        """Displays all items dynamically based on object attributes."""
        if not self.inventory_shop:
            print(Fore.RED + "⚠️ No items available in this shop yet!" + Style.RESET_ALL)
            return

        print(Fore.YELLOW + f"\n========= {category_name.upper()} =========" + Style.RESET_ALL)
        for i, item in enumerate(self.inventory_shop, 1):
            rarity = getattr(item, "rarity", "Common")
            color = {
                "Common": Fore.WHITE,
                "Uncommon": Fore.GREEN,
                "Rare": Fore.BLUE,
                "Epic": Fore.MAGENTA,
                "Legendary": Fore.YELLOW,
            }.get(rarity, Fore.WHITE)

            # Detect stats dynamically
            stats = []
            for attr in ["damage", "defense", "heals"]:
                if hasattr(item, attr):
                    stats.append(f"{attr.title()}: +{getattr(item, attr)}")

            stat_text = " | ".join(stats) if stats else "No Bonus"
            print(
                f"{i}. {color}{item.name}{Style.RESET_ALL} | {stat_text} | 💰 {item.value} | {color}{rarity}{Style.RESET_ALL}"
            )
        print(Fore.YELLOW + "=" * 40 + "\n" + Style.RESET_ALL)


# ==============================
# ⚔️ SWORD SHOP
# ==============================
class shop_sword(Shop):
    def __init__(self):
        super().__init__()

    def stock_sword_dagger(self):
        self.stock_items([
            Weapon("Swiftfang", "Dagger", 12, 70),
            Weapon("Shadow Pierce", "Dagger", 20, 110),
            Weapon("Silent Fang", "Dagger", 17, 95),
            Weapon("Ironbite", "Dagger", 10, 55),
            Weapon("Storm Edge", "Dagger", 25, 140),
        ])

    def stock_sword_katana(self):
        self.stock_items([
            Weapon("Kurohana", "Katana", 20, 100),
            Weapon("Tsukikage", "Katana", 30, 140),
            Weapon("Akatsuki Blade", "Katana", 35, 170),
            Weapon("Ryuuzan", "Katana", 18, 90),
            Weapon("Hikarimaru", "Katana", 28, 130),
        ])

    def stock_sword_great_sword(self):
        self.stock_items([
            Weapon("Titanbreaker", "Great Sword", 22, 120),
            Weapon("Oblivion Fang", "Great Sword", 35, 170),
            Weapon("Dragon’s Wrath", "Great Sword", 45, 210),
            Weapon("Judgment Edge", "Great Sword", 18, 95),
            Weapon("Gravemourn", "Great Sword", 30, 150),
        ])


# ==============================
# 🏹 BOW SHOP
# ==============================
class shop_bow(Shop):
    def __init__(self):
        super().__init__()

    def stock_bows(self):
        self.stock_items([
            Weapon("Photon Arc", "Tech Bow", 28, 150),
            Weapon("Nova String", "Tech Bow", 35, 180),
            Weapon("Ionflare", "Tech Bow", 42, 220),
            Weapon("Pulse Bow", "Tech Bow", 20, 120),
            Weapon("Plasma Piercer", "Tech Bow", 25, 140),
        ])


# ==============================
# 📜 GRIMOIRE SHOP
# ==============================
class shop_grimoire(Shop):
    def __init__(self):
        super().__init__()

    def stock_grimoires(self):
        self.stock_items([
            Weapon("Flame Codex", "Grimoire", 25, 120),
            Weapon("Aqua Tome", "Grimoire", 30, 140),
            Weapon("Terra Scroll", "Grimoire", 35, 160),
            Weapon("Tempest Grimoire", "Grimoire", 40, 180),
            Weapon("Infernal Codex", "Grimoire", 45, 200),
        ])


# ==============================
# 💫 STAFF SHOP
# ==============================
class shop_staff(Shop):
    def __init__(self):
        super().__init__()

    def stock_staffs(self):
        self.stock_items([
            Weapon("Novice Staff", "Staff", 15, 80),
            Weapon("Cleric Rod", "Staff", 20, 110),
            Weapon("Sanctum Wand", "Staff", 25, 140),
            Weapon("Seraph’s Blessing", "Staff", 32, 180),
            Weapon("Divine Lumina", "Staff", 40, 220),
        ])


# ==============================
# 🛡️ ARMOR SHOP
# ==============================
class shop_armor(Shop):
    def __init__(self):
        super().__init__()

    def stock_armors(self):
        self.stock_items([
            Armor("Leather Vest", 8, "Light", 70),
            Armor("Shadow Cloak", 12, "Light", 100),
            Armor("Wind Dancer Garb", 18, "Light", 130),
            Armor("Nightveil Shroud", 25, "Light", 180),
        ])


# ==============================
# 💊 POTION SHOP
# ==============================
class shop_potion(Shop):
    def __init__(self):
        super().__init__()

    def stock_health_potions(self):
        self.stock_items([
            Health_Potions("Small Potion", 25, 30),
            Health_Potions("Medium Potion", 50, 60),
            Health_Potions("Large Potion", 90, 100),
            Health_Potions("Mega Potion", 130, 150),
        ])
