import pytest

from Shop import Shop
from items import Weapon, Armor, Health_Potions


def test_shop_add_stock_clear():
    shop = Shop("Test Shop")
    sword = Weapon("Sword", "Sharp", damage=5, value=10)
    armor = Armor("Leather", defense=2, defense_type="Blunt", value=8)
    potion = Health_Potions("Potion", value=3, heals=10)

    shop.add_item(sword)
    assert shop.get_item_count() == 1

    shop.stock_items([armor, potion])
    assert shop.get_item_count() == 3

    shop.clear_inventory()
    assert shop.get_item_count() == 0