"""
Inventory management system for RPG Game
Handles item storage, sorting, and manipulation
"""

from typing import List, Optional
from items import Items


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
        """Check if inventory has reached capacity"""
        if self.max_capacity is None:
            return False
        return len(self.items) >= self.max_capacity
    
    def add_item(self, item: Items) -> bool:
        """
        Add an item to the inventory
        
        Args:
            item: Item object to add
            
        Returns:
            bool: True if added successfully, False if inventory full
        """
        if self. is_full():
            print("Inventory is full!  Cannot add more items.")
            return False
        
        self.items.append(item)
        item_name = getattr(item, 'name', 'Item')
        print(f"{item_name} has been added to the inventory.")
        return True
    
    def remove_item(self, item: Items) -> bool:
        """
        Remove an item from the inventory
        
        Args:
            item: Item object to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if item in self.items:
            self. items.remove(item)
            item_name = getattr(item, 'name', 'Item')
            print(f"{item_name} has been removed from the inventory.")
            return True
        else:
            item_name = getattr(item, 'name', 'Item')
            print(f"{item_name} is not in the inventory.")
            return False
    
    def list_items(self):
        """Display all items in inventory with index numbers"""
        if not self.items:
            print("Inventory is empty.")
            return
        
        print("Inventory items:")
        for idx, item in enumerate(self.items, 1):
            item_name = getattr(item, 'name', 'Unknown Item')
            item_value = getattr(item, 'value', 'Unknown Value')
            print(f"{idx}. {item_name} (Value: {item_value})")
    
    def sort_items(self, by_name: bool = True):
        """
        Sort inventory items
        
        Args:
            by_name: If True, sort alphabetically by name. 
                    If False, sort by value (descending)
        """
        if by_name:
            self.items.sort(key=lambda x: getattr(x, 'name', ''))
        else:
            self.items.sort(key=lambda x: getattr(x, 'value', 0), reverse=True)
    
    def use_consumable(self, item: Items, entity) -> bool:
        """
        Use a consumable item on an entity
        
        Args:
            item: The consumable item to use
            entity: Target character/entity
            
        Returns:
            bool: True if used successfully
        """
        if item not in self.items:
            item_name = getattr(item, 'name', 'Item')
            print(f"{item_name} is not in the inventory.")
            return False
        
        try:
            item.uses(entity)
            self.items.remove(item)
            return True
        except AttributeError:
            print("This item can't be used.")
            return False
    
    def get_item_by_index(self, index: int) -> Optional[Items]:
        """
        Get item by its display index (1-based)
        
        Args:
            index: Display index (1 to len(items))
            
        Returns:
            Item if found, None otherwise
        """
        if 1 <= index <= len(self.items):
            return self.items[index - 1]
        return None
    
    def count_items(self) -> int:
        """Return the number of items in inventory"""
        return len(self.items)
    
    def __len__(self) -> int:
        """Allow len() to be called on inventory"""
        return len(self.items)
    
    def __bool__(self) -> bool:
        """Allow inventory to be used in boolean context"""
        return len(self.items) > 0
