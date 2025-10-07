class Inventory():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"{item.name} has been added to the inventory.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item.name} has been removed from the inventory.")
        else:
            print(f"{item.name} is not in the inventory.")

    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Inventory items:")
            for idx, item in enumerate(self.items, 1):
                print(f"{idx}. {item.name} (Value: {getattr(item, 'value', '-')})")

    def use_consumeable(self,item,entity):
        if item in self.items:
            self.item.uses(entity)
            self.items.remove(item)
        else :
            print(f"{item.name} is not in the inventory.")
        