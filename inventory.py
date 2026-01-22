"""
Inventory management system for RPG Game
Refactored to follow Single Responsibility Principle
Each class has one clear responsibility
"""

from typing import List, Optional
from items import Items


# ==============================
# 1. ITEM STORAGE - Manages item collection
# ==============================

class ItemStorage:
    """
    Responsible for storing and retrieving items
    Single Responsibility: Managing the item collection
    """
    
    def __init__(self):
        """Initialize an empty item storage"""
        self._items: List[Items] = []
    
    def add(self, item: Items) -> None:
        """Add an item to storage"""
        self._items.append(item)
    
    def remove(self, item: Items) -> bool:
        """
        Remove an item from storage
        
        Returns:
            bool: True if removed, False if not found
        """
        if item in self._items:
            self._items.remove(item)
            return True
        return False
    
    def contains(self, item: Items) -> bool:
        """Check if item exists in storage"""
        return item in self._items
    
    def get_by_index(self, index: int) -> Optional[Items]:
        """
        Get item by index (0-based)
        
        Args:
            index: Zero-based index
            
        Returns:
            Item if found, None otherwise
        """
        if 0 <= index < len(self._items):
            return self._items[index]
        return None
    
    def get_all(self) -> List[Items]:
        """Return all items"""
        return self._items.copy()
    
    def count(self) -> int:
        """Return the number of items"""
        return len(self._items)
    
    def is_empty(self) -> bool:
        """Check if storage is empty"""
        return len(self._items) == 0
    
    def clear(self) -> None:
        """Remove all items"""
        self._items.clear()


# ==============================
# 2. CAPACITY MANAGER - Manages inventory limits
# ==============================

class CapacityManager:
    """
    Responsible for managing inventory capacity limits
    Single Responsibility: Capacity validation and limits
    """
    
    def __init__(self, max_capacity: Optional[int] = None):
        """
        Initialize capacity manager
        
        Args:
            max_capacity: Optional maximum item limit (None = unlimited)
        """
        self.max_capacity = max_capacity
    
    def is_full(self, current_count: int) -> bool:
        """
        Check if capacity has been reached
        
        Args:
            current_count: Current number of items
            
        Returns:
            bool: True if at capacity, False otherwise
        """
        if self.max_capacity is None:
            return False
        return current_count >= self.max_capacity
    
    def can_add(self, current_count: int, amount: int = 1) -> bool:
        """
        Check if items can be added
        
        Args:
            current_count: Current number of items
            amount: Number of items to add
            
        Returns:
            bool: True if there's space, False otherwise
        """
        if self.max_capacity is None:
            return True
        return current_count + amount <= self.max_capacity
    
    def get_available_space(self, current_count: int) -> Optional[int]:
        """
        Get remaining capacity
        
        Returns:
            int: Available space, or None if unlimited
        """
        if self.max_capacity is None:
            return None
        return max(0, self.max_capacity - current_count)


# ==============================
# 3. ITEM SORTER - Handles item sorting
# ==============================

class ItemSorter:
    """
    Responsible for sorting items by different criteria
    Single Responsibility: Item sorting logic
    """
    
    @staticmethod
    def sort_by_name(items: List[Items], reverse: bool = False) -> List[Items]:
        """
        Sort items alphabetically by name
        
        Args:
            items: List of items to sort
            reverse: If True, sort in descending order
            
        Returns:
            Sorted list of items
        """
        return sorted(items, key=lambda x: getattr(x, 'name', ''), reverse=reverse)
    
    @staticmethod
    def sort_by_value(items: List[Items], reverse: bool = True) -> List[Items]:
        """
        Sort items by value
        
        Args:
            items: List of items to sort
            reverse: If True, sort high to low (default)
            
        Returns:
            Sorted list of items
        """
        return sorted(items, key=lambda x: getattr(x, 'value', 0), reverse=reverse)
    
    @staticmethod
    def sort_by_type(items: List[Items]) -> List[Items]:
        """
        Sort items by their class type
        
        Args:
            items: List of items to sort
            
        Returns:
            Sorted list of items
        """
        return sorted(items, key=lambda x: x.__class__.__name__)


# ==============================
# 4. ITEM USER - Handles item usage
# ==============================

class ItemUser:
    """
    Responsible for using consumable items
    Single Responsibility: Item usage logic
    """
    
    @staticmethod
    def use_item(item: Items, entity) -> bool:
        """
        Use an item on an entity
        
        Args:
            item: The item to use
            entity: Target character/entity
            
        Returns:
            bool: True if used successfully, False otherwise
        """
        try:
            if hasattr(item, 'uses'):
                item.uses(entity)
                return True
            return False
        except (AttributeError, Exception):
            return False


# ==============================
# 5. INVENTORY DISPLAY - Handles display/formatting
# ==============================

class InventoryDisplay:
    """
    Responsible for displaying inventory information
    Single Responsibility: Formatting and displaying inventory data
    """
    
    @staticmethod
    def format_item(item: Items, index: int) -> str:
        """
        Format a single item for display
        
        Args:
            item: Item to format
            index: Display index (1-based)
            
        Returns:
            Formatted string
        """
        item_name = getattr(item, 'name', 'Unknown Item')
        item_value = getattr(item, 'value', 'Unknown Value')
        return f"{index}. {item_name} (Value: {item_value})"
    
    @staticmethod
    def display_items(items: List[Items]) -> None:
        """
        Display all items in a formatted list
        
        Args:
            items: List of items to display
        """
        if not items:
            print("Inventory is empty.")
            return
        
        print("Inventory items:")
        for idx, item in enumerate(items, 1):
            print(InventoryDisplay.format_item(item, idx))
    
    @staticmethod
    def display_message(message: str) -> None:
        """Display a message to the user"""
        print(message)


# ==============================
# 6. INVENTORY - Coordinates all components
# ==============================

class Inventory:
    """
    Main Inventory class that coordinates all components
    Single Responsibility: Coordinating inventory operations
    
    This class delegates specific tasks to specialized components:
    - ItemStorage: Manages the item collection
    - CapacityManager: Handles capacity limits
    - ItemSorter: Sorts items
    - ItemUser: Uses consumable items
    - InventoryDisplay: Displays inventory information
    """
    
    def __init__(self, max_capacity: Optional[int] = None):
        """
        Initialize inventory with all components
        
        Args:
            max_capacity: Optional maximum item limit (None = unlimited)
        """
        self._storage = ItemStorage()
        self._capacity = CapacityManager(max_capacity)
        self._sorter = ItemSorter()
        self._user = ItemUser()
        self._display = InventoryDisplay()
    
    @property
    def items(self) -> List[Items]:
        """Get all items (for backward compatibility)"""
        return self._storage.get_all()
    
    def is_full(self) -> bool:
        """Check if inventory has reached capacity"""
        return self._capacity.is_full(self._storage.count())
    
    def add_item(self, item: Items) -> bool:
        """
        Add an item to the inventory
        
        Args:
            item: Item object to add
            
        Returns:
            bool: True if added successfully, False if inventory full
        """
        if self.is_full():
            self._display.display_message("Inventory is full! Cannot add more items.")
            return False
        
        self._storage.add(item)
        item_name = getattr(item, 'name', 'Item')
        self._display.display_message(f"{item_name} has been added to the inventory.")
        return True
    
    def remove_item(self, item: Items) -> bool:
        """
        Remove an item from the inventory
        
        Args:
            item: Item object to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        item_name = getattr(item, 'name', 'Item')
        
        if self._storage.remove(item):
            self._display.display_message(f"{item_name} has been removed from the inventory.")
            return True
        else:
            self._display.display_message(f"{item_name} is not in the inventory.")
            return False
    
    def list_items(self) -> None:
        """Display all items in inventory with index numbers"""
        self._display.display_items(self._storage.get_all())
    
    def sort_items(self, by_name: bool = True) -> None:
        """
        Sort inventory items
        
        Args:
            by_name: If True, sort alphabetically by name. 
                    If False, sort by value (descending)
        """
        items = self._storage.get_all()
        
        if by_name:
            sorted_items = self._sorter.sort_by_name(items)
        else:
            sorted_items = self._sorter.sort_by_value(items)
        
        # Update storage with sorted items
        self._storage.clear()
        for item in sorted_items:
            self._storage.add(item)
    
    def use_consumable(self, item: Items, entity) -> bool:
        """
        Use a consumable item on an entity
        
        Args:
            item: The consumable item to use
            entity: Target character/entity
            
        Returns:
            bool: True if used successfully
        """
        if not self._storage.contains(item):
            item_name = getattr(item, 'name', 'Item')
            self._display.display_message(f"{item_name} is not in the inventory.")
            return False
        
        if self._user.use_item(item, entity):
            self._storage.remove(item)
            return True
        else:
            self._display.display_message("This item can't be used.")
            return False
    
    def get_item_by_index(self, index: int) -> Optional[Items]:
        """
        Get item by its display index (1-based)
        
        Args:
            index: Display index (1 to len(items))
            
        Returns:
            Item if found, None otherwise
        """
        return self._storage.get_by_index(index - 1)
    
    def count_items(self) -> int:
        """Return the number of items in inventory"""
        return self._storage.count()
    
    def __len__(self) -> int:
        """Allow len() to be called on inventory"""
        return self._storage.count()
    
    def __bool__(self) -> bool:
        """Allow inventory to be used in boolean context"""
        return not self._storage.is_empty()
