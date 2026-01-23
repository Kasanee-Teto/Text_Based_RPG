from inventory import Inventory
from items import Item

class DummyItem(Item):
    def __init__(self, name):
        super().__init__(name, 10)

def test_add_and_remove_items():
    inv = Inventory()
    sword = DummyItem("Sword")
    shield = DummyItem("Shield")

    inv.add_item(sword)
    inv.add_item(shield)
    assert sword in inv.items
    assert shield in inv.items

    inv.remove_item(sword)
    assert sword not in inv.items
    assert shield in inv.items