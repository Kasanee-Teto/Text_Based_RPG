from inventory import Inventory


class DummyItem:
    def __init__(self, name):
        self.name = name


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