class Inventory():
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        try:
            name = item.name
        except AttributeError:
            name = "Item"
        print(f"{name} has been added to the inventory.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            try:
                name = item.name
            except AttributeError:
                name = "Item"
            print(f"{name} has been removed from the inventory.")
        else:
            try:
                name = item.name
            except AttributeError:
                name = "Item"
            print(f"{name} is not in the inventory.")

    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Inventory items:")
            for idx, item in enumerate(self.items, 1):
                try:
                    name = item.name
                except AttributeError:
                    name = "Unknown Item"
                try :
                    value = item.value
                except AttributeError:
                    value = "-"
                print(f"{idx}. {name} (Value: {value})")

    def use_consumeable(self,item,entity):
        if item in self.items:
            try:
                item.uses(entity)
                self.items.remove(item)
            except AttributeError:
                print("This intem can't be used.")
        else :
            try:
                name = item.name
            except AttributeError:
                name = "Item"
            print(f"{name} is not in the inventory.")