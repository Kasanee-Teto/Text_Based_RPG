from typing import List, Optional
from items import Item, Consumable

class Inventory:
    """
    Manages a collection of items for a character
    
    Attributes:
        items (List[Items]): List of item objects
        max_capacity (int): Maximum number of items (optional limit)
    """
    
    def __init__(self, max_capacity: Optional[int] = None):
        """
        Initialize an empty inventory
        
        Args:
            max_capacity: Optional maximum item limit (None = unlimited)
        """
        self. items: List[Items] = []
        self.max_capacity = max_capacity
    
    def is_full(self) -> bool:
    
    def add_item(self, item: Item) -> bool:
        if self.is_full():
            print("Inventory is full!")
            return False
        self.items.append(item)
        print(f"{item.name} added to inventory.")
        return True
    
    def remove_item(self, item: Item) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
            return
        print("Inventory items:")
        for idx, item in enumerate(self.items, 1):
            print(f"{idx}. {item.name} (Value: {item.value})")
    
    def sort_items(self, by_name: bool = True):
        if by_name:
            self.items.sort(key=lambda x: x.name)
        else:
            self.items.sort(key=lambda x: x.value, reverse=True)
    
    def use_consumable(self, item: Item, entity) -> bool:
        if item not in self.items: return False
        if isinstance(item, Consumable):
            item.use(entity)
            self.items.remove(item)
            return True
        return False
    
    def get_item_by_index(self, index: int) -> Optional[Item]:
        if 1 <= index <= len(self.items):
            return self.items[index - 1]
        return None