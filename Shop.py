# ==============================
# 📜 SHOP SYSTEM
# ==============================
from items import *
class shop:
    def __init__(self):
        self.inventory_shop = []  # semua item tersimpan di sini

        def show_items(self):
            print("-------------------------------------------------")
            for i, item in enumerate(self.inventory_shop, 1):
                stats = []
                if "attack_bonus" in item:
                    stats.append(f"ATK +{item['attack_bonus']}")
                if "defense_bonus" in item:
                    stats.append(f"DEF +{item['defense_bonus']}")
                if "magic_power" in item:
                    stats.append(f"MAG +{item['magic_power']}")
                if "heal_amount" in item:
                    stats.append(f"Heal +{item['heal_amount']}")
                print(f"{i}. {item['name']} | {' | '.join(stats)} | 💰 {item['price']} | Stock: {item['stock']} | {item['rarity']}")
            print("-------------------------------------------------")


# ==============================
# ⚔️ SHOP - SWORD
# ==============================
class shop_sword(shop):
    def __init__(self):
        super().__init__()

    def stock_sword_dagger(self):
        dagger_items = [
            {"name": "Swiftfang", "type": "Dagger", "attack_bonus": 12, "price": 70, "stock": 8, "rarity": "Common"},
            {"name": "Shadow Pierce", "type": "Dagger", "attack_bonus": 20, "price": 110, "stock": 5, "rarity": "Rare"},
            {"name": "Silent Fang", "type": "Dagger", "attack_bonus": 17, "price": 95, "stock": 6, "rarity": "Uncommon"},
            {"name": "Ironbite", "type": "Dagger", "attack_bonus": 10, "price": 55, "stock": 9, "rarity": "Common"},
            {"name": "Storm Edge", "type": "Dagger", "attack_bonus": 25, "price": 140, "stock": 3, "rarity": "Epic"},
        ]
        self.inventory_shop.extend(dagger_items)

    def stock_sword_katana(self):
        # Kurohana (黒花) = Bunga hitam
        # Tsukikage (月影) = Bayangan Bulan
        # Akatsuki Blade (暁の刃) = Pedang Fajar
        # Ryuuzan (龍斬) = Dragon Cleaver
        # Hikarimaru (光丸) = Lingkaran Cahaya
        katana_items = [
            {"name": "Kurohana (黒花)", "type": "Katana", "attack_bonus": 20, "price": 100, "stock": 6, "rarity": "Uncommon"},
            {"name": "Tsukikage (月影)", "type": "Katana", "attack_bonus": 30, "price": 140, "stock": 4, "rarity": "Rare"},
            {"name": "Akatsuki Blade (暁の刃)", "type": "Katana", "attack_bonus": 35, "price": 170, "stock": 3, "rarity": "Epic"},
            {"name": "Ryuuzan (龍斬)", "type": "Katana", "attack_bonus": 18, "price": 90, "stock": 8, "rarity": "Common"},
            {"name": "Hikarimaru (光丸)", "type": "Katana", "attack_bonus": 28, "price": 130, "stock": 5, "rarity": "Rare"},
        ]
        self.inventory_shop.extend(katana_items)

    def stock_sword_great_sword(self):
        great_sword_items = [
            {"name": "Titanbreaker", "type": "Great Sword", "attack_bonus": 22, "price": 120, "stock": 5, "rarity": "Uncommon"},
            {"name": "Oblivion Fang", "type": "Great Sword", "attack_bonus": 35, "price": 170, "stock": 3, "rarity": "Rare"},
            {"name": "Dragon’s Wrath", "type": "Great Sword", "attack_bonus": 45, "price": 210, "stock": 2, "rarity": "Epic"},
            {"name": "Judgment Edge", "type": "Great Sword", "attack_bonus": 18, "price": 95, "stock": 7, "rarity": "Common"},
            {"name": "Gravemourn", "type": "Great Sword", "attack_bonus": 30, "price": 150, "stock": 4, "rarity": "Rare"},
        ]
        self.inventory_shop.extend(great_sword_items)


# ==============================
# 🏹 SHOP - BOW
# ==============================
class shop_bow(shop):
    def __init__(self):
        super().__init__()


    # 🧠 Bow modern yang presisi dan damage tinggi, tapi mahal & stok sedikit
    def stock_tech_bow(self):
        tech_bow = [
            {"name": "Photon Arc", "type": "Tech Bow", "attack_bonus": 28, "price": 150, "stock": 4, "rarity": "Rare"},   
            {"name": "Nova String", "type": "Tech Bow", "attack_bonus": 35, "price": 180, "stock": 3, "rarity": "Epic"},  
            {"name": "Ionflare", "type": "Tech Bow", "attack_bonus": 42, "price": 220, "stock": 2, "rarity": "Legendary"},
            {"name": "Pulse Bow", "type": "Tech Bow", "attack_bonus": 20, "price": 120, "stock": 6, "rarity": "Uncommon"},
            {"name": "Plasma Piercer", "type": "Tech Bow", "attack_bonus": 25, "price": 140, "stock": 5, "rarity": "Rare"},
        ]
        self.inventory_shop.extend(tech_bow)

    # ⚙️ Crossbow: power tinggi, tapi berat dan lambat → stok lebih sedikit
    def stock_crossbow(self):
        crossbow = [
            {"name": "Ironbolt", "type": "Crossbow", "attack_bonus": 22, "price": 100, "stock": 6, "rarity": "Common"},    
            {"name": "Steel Fang", "type": "Crossbow", "attack_bonus": 28, "price": 130, "stock": 5, "rarity": "Rare"},   
            {"name": "Thunderbolt", "type": "Crossbow", "attack_bonus": 35, "price": 160, "stock": 3, "rarity": "Epic"},  
            {"name": "Obsidian Quarrel", "type": "Crossbow", "attack_bonus": 40, "price": 200, "stock": 2, "rarity": "Legendary"}, 
            {"name": "Viper’s Nest", "type": "Crossbow", "attack_bonus": 30, "price": 145, "stock": 4, "rarity": "Rare"},
        ]
        self.inventory_shop.extend(crossbow)

    # 🏹 Recurve Bow: klasik dan seimbang, cocok untuk karakter early–mid game
    def stock_recuve_bow(self):
        recuve_bow = [
            {"name": "Oak Whisper", "type": "Recurve Bow", "attack_bonus": 14, "price": 70, "stock": 9, "rarity": "Common"}, 
            {"name": "Windpiercer", "type": "Recurve Bow", "attack_bonus": 18, "price": 90, "stock": 8,  "rarity": "Common"}, 
            {"name": "Silver Gale", "type": "Recurve Bow", "attack_bonus": 22, "price": 110, "stock": 6, "rarity": "Uncommon"},
            {"name": "Eagle’s Cry", "type": "Recurve Bow", "attack_bonus": 28, "price": 135, "stock": 4,  "rarity": "Rare"},
            {"name": "Moonshadow", "type": "Recurve Bow", "attack_bonus": 33, "price": 160, "stock": 3, "rarity": "Epic"},
        ]
        self.inventory_shop.extend(recuve_bow)


# ==============================
# 📜 SHOP - GRIMOIRE (Mage)
# ==============================
class shop_grimoire(shop):
    def __init__(self):
        super().__init__()


    def stock_elemental_grimoire(self):
        elemental_grimoire = [
        {"name": "Flame Codex", "type": "Elemental Grimoire", "magic_power": 25, "price": 120, "stock": 5, "rarity": "Common"},
        {"name": "Aqua Tome", "type": "Elemental Grimoire", "magic_power": 30, "price": 140, "stock": 4, "rarity": "Uncommon"},
        {"name": "Terra Scroll", "type": "Elemental Grimoire", "magic_power": 35, "price": 160, "stock": 3, "rarity": "Rare"},
        {"name": "Tempest Grimoire", "type": "Elemental Grimoire", "magic_power": 40, "price": 180, "stock": 2, "rarity": "Epic"},
        {"name": "Infernal Codex", "type": "Elemental Grimoire", "magic_power": 45, "price": 200, "stock": 2, "rarity": "Legendary"},
    ]
        self.inventory_shop.extend(elemental_grimoire)

    def stock_dark_grimoire(self):
        dark_grimoire = [
            {"name": "Shadow Manuscript", "type": "Dark Grimoire", "magic_power": 25, "price": 120, "stock": 5, "rarity": "Common"},
            {"name": "Cursed Chronicle", "type": "Dark Grimoire", "magic_power": 30, "price": 140, "stock": 4, "rarity": "Uncommon"},
            {"name": "Abyssal Scripture", "type": "Dark Grimoire", "magic_power": 35, "price": 160, "stock": 3, "rarity": "Rare"},
            {"name": "Necro Codex", "type": "Dark Grimoire", "magic_power": 42, "price": 185, "stock": 2, "rarity": "Epic"},
            {"name": "Soulbinder Tome", "type": "Dark Grimoire", "magic_power": 50, "price": 210, "stock": 1, "rarity": "Legendary"},
        ]
        self.inventory_shop.extend(dark_grimoire)

    def stock_arcane_grimoire(self):
        arcane_grimoire = [
            {"name": "Mystic Compendium", "type": "Arcane Grimoire", "magic_power": 28, "price": 130, "stock": 5, "rarity": "Common"},
            {"name": "Astral Codex", "type": "Arcane Grimoire", "magic_power": 34, "price": 150, "stock": 4, "rarity": "Uncommon"},
            {"name": "Ethereal Lexicon", "type": "Arcane Grimoire", "magic_power": 40, "price": 175, "stock": 3, "rarity": "Rare"},
            {"name": "Runebound Tome", "type": "Arcane Grimoire", "magic_power": 46, "price": 200, "stock": 2, "rarity": "Epic"},
            {"name": "Celestial Archive", "type": "Arcane Grimoire", "magic_power": 52, "price": 230, "stock": 1, "rarity": "Legendary"},
        ]
        self.inventory_shop.extend(arcane_grimoire)


# ==============================
# 💫 SHOP - STAFF (Healer)
# ==============================
class shop_staff(shop):
    def __init__(self):
        super().__init__()


    def stock_healing_staff(self):
        healing_staff = [
        {"name": "Novice Staff", "type": "Healing Staff", "magic_power": 15, "healing_power": 25, "price": 80, "stock": 7, "rarity": "Common"},
        {"name": "Cleric Rod", "type": "Healing Staff", "magic_power": 20, "healing_power": 35, "price": 110, "stock": 5, "rarity": "Uncommon"},
        {"name": "Sanctum Wand", "type": "Healing Staff", "magic_power": 25, "healing_power": 45, "price": 140, "stock": 4, "rarity": "Rare"},
        {"name": "Seraph’s Blessing", "type": "Healing Staff", "magic_power": 32, "healing_power": 60, "price": 180, "stock": 2, "rarity": "Epic"},
        {"name": "Divine Lumina", "type": "Healing Staff", "magic_power": 40, "healing_power": 75, "price": 220, "stock": 1, "rarity": "Legendary"},
    ]
        self.inventory_shop.extend(healing_staff)

    def stock_elemental_staff(self):
        elemental_staff = [
            {"name": "Ember Staff", "type": "Elemental Staff", "magic_power": 25, "price": 120, "stock": 5, "rarity": "Common"},
            {"name": "Frostbinder", "type": "Elemental Staff", "magic_power": 35, "price": 150, "stock": 4, "rarity": "Uncommon"},
            {"name": "Thundercaller", "type": "Elemental Staff", "magic_power": 45, "price": 180, "stock": 3, "rarity": "Rare"},
            {"name": "Voltryn", "type": "Elemental Staff", "magic_power": 55, "price": 210, "stock": 2, "rarity": "Epic"},
            {"name": "Infernia", "type": "Elemental Staff", "magic_power": 65, "price": 250, "stock": 1, "rarity": "Legendary"},
        ]
        self.inventory_shop.extend(elemental_staff)

    def stock_dark_staff(self):
        dark_staff = [
            {"name": "Shade Wand", "type": "Dark Staff", "magic_power": 28, "price": 130, "stock": 5, "rarity": "Common"},
            {"name": "Soulpiercer", "type": "Dark Staff", "magic_power": 38, "price": 160, "stock": 4, "rarity": "Uncommon"},
            {"name": "Grimreach", "type": "Dark Staff", "magic_power": 48, "price": 190, "stock": 3, "rarity": "Rare"},
            {"name": "Necrotic Staff", "type": "Dark Staff", "magic_power": 60, "price": 230, "stock": 2, "rarity": "Epic"},
            {"name": "Deathbinder", "type": "Dark Staff", "magic_power": 70, "price": 270, "stock": 1, "rarity": "Legendary"},
        ]
        self.inventory_shop.extend(dark_staff)

# ==============================
# 🛡️ SHOP - ARMOR
# ==============================
class shop_armor(shop):
    def __init__(self):
        super().__init__()

    def stock_light_armor(self):
        light_armor_items = [
            {"name": "Leather Vest", "type": "Light Armor", "defense_bonus": 8, "price": 70, "stock": 8, "rarity": "Common"},
            {"name": "Shadow Cloak", "type": "Light Armor", "defense_bonus": 12, "price": 100, "stock": 6, "rarity": "Uncommon"},
            {"name": "Wind Dancer Garb", "type": "Light Armor", "defense_bonus": 18, "price": 130, "stock": 4, "rarity": "Rare"},
            {"name": "Nightveil Shroud", "type": "Light Armor", "defense_bonus": 25, "price": 180, "stock": 2, "rarity": "Epic"},
        ]
        self.inventory_shop.extend(light_armor_items)

    def stock_medium_armor(self):
        medium_armor_items = [
            {"name": "Ironplate", "type": "Medium Armor", "defense_bonus": 12, "price": 90, "stock": 7, "rarity": "Common"},
            {"name": "Battleforged Mail", "type": "Medium Armor", "defense_bonus": 20, "price": 130, "stock": 5, "rarity": "Uncommon"},
            {"name": "Vanguard Guard", "type": "Medium Armor", "defense_bonus": 28, "price": 160, "stock": 3, "rarity": "Rare"},
            {"name": "Crimson Bulwark", "type": "Medium Armor", "defense_bonus": 35, "price": 200, "stock": 2, "rarity": "Epic"},
        ]
        self.inventory_shop.extend(medium_armor_items)

    def stock_heavy_armor(self):
        heavy_armor_items = [
            {"name": "Steelplate", "type": "Heavy Armor", "defense_bonus": 18, "price": 120, "stock": 6, "rarity": "Common"},
            {"name": "Warlord’s Chest", "type": "Heavy Armor", "defense_bonus": 30, "price": 170, "stock": 4, "rarity": "Uncommon"},
            {"name": "Dragonscale Aegis", "type": "Heavy Armor", "defense_bonus": 40, "price": 210, "stock": 2, "rarity": "Rare"},
            {"name": "Eternal Fortress", "type": "Heavy Armor", "defense_bonus": 50, "price": 250, "stock": 1, "rarity": "Legendary"},
        ]
        self.inventory_shop.extend(heavy_armor_items)


# ==============================
# 💊 SHOP - HEALTH POTION
# ==============================
class shop_potion(shop):
    def __init__(self):
        super().__init__()

    def stock_health_potions(self):
        potion_items = [
            {"name": "Small Potion", "type": "Potion", "heal_amount": 30, "price": 25, "stock": 15, "rarity": "Common"},
            {"name": "Medium Potion", "type": "Potion", "heal_amount": 60, "price": 50, "stock": 10, "rarity": "Uncommon"},
            {"name": "Large Potion", "type": "Potion", "heal_amount": 100, "price": 90, "stock": 6, "rarity": "Rare"},
            {"name": "Mega Potion", "type": "Potion", "heal_amount": 150, "price": 130, "stock": 3, "rarity": "Epic"},
        ]
        self.inventory_shop.extend(potion_items)
