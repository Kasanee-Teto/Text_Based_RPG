"""
Save/Load system for RPG Game
Handles player data persistence using pickle serialization
"""

import os
import pickle
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Character. Character_RPG import Player


# ==============================
# CONFIGURATION
# ==============================

SAVE_DIRECTORY = "save"
SAVE_EXTENSION = ".pkl"


# ==============================
# INITIALIZATION
# ==============================

def initialize_save_system():
    """Create save directory if it doesn't exist"""
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)


initialize_save_system()


# ==============================
# SAVE FUNCTIONS
# ==============================

def save_game(player: 'Player', custom_filename: Optional[str] = None) -> bool:
    """
    Save player data to file
    
    Args:
        player: Player object to save
        custom_filename: Optional custom filename (without extension)
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        filename = custom_filename if custom_filename else player.name
        filepath = os.path.join(SAVE_DIRECTORY, f"{filename}{SAVE_EXTENSION}")
        
        with open(filepath, "wb") as f:
            pickle.dump(player, f)
        
        print(f"💾 Game saved successfully for {player.name}!")
        return True
    
    except Exception as e:
        print(f"❌ Error saving game: {e}")
        return False


def save_games(player: 'Player'):
    """Legacy function name for compatibility"""
    return save_game(player)


# ==============================
# LOAD FUNCTIONS
# ==============================

def get_save_files() -> list:
    """
    Get list of all save files
    
    Returns:
        list: List of save filenames (without extension)
    """
    try:
        files = os.listdir(SAVE_DIRECTORY)
        saves = [f.replace(SAVE_EXTENSION, '') for f in files if f.endswith(SAVE_EXTENSION)]
        return saves
    except Exception as e:
        print(f"❌ Error reading save directory: {e}")
        return []


def load_game(filename: Optional[str] = None) -> Optional['Player']:
    """
    Load player data from file
    
    Args:
        filename: Optional specific filename to load (without extension)
                 If None, prompts user to choose
    
    Returns:
        Player object if loaded successfully, None otherwise
    """
    saves = get_save_files()
    
    if not saves:
        print("❌ No saved games found.")
        return None
    
    # If specific filename provided
    if filename:
        if filename in saves:
            return _load_save_file(filename)
        else:
            print(f"❌ Save file '{filename}' not found.")
            return None
    
    # Otherwise, show menu
    print("\n" + "=" * 50)
    print("📂 Choose a save file:".center(50))
    print("=" * 50)
    
    for i, save in enumerate(saves, 1):
        print(f"{i}. {save}")
    
    print("=" * 50)
    
    try:
        choice = int(input("➤ Enter number: "))
        if 1 <= choice <= len(saves):
            return _load_save_file(saves[choice - 1])
        else:
            print("❌ Invalid choice!")
            return None
    
    except ValueError:
        print("❌ Invalid input! Please enter a number.")
        return None


def _load_save_file(filename: str) -> Optional['Player']:
    """
    Internal function to load a specific save file
    
    Args:
        filename: Filename without extension
        
    Returns:
        Player object if successful, None otherwise
    """
    try:
        filepath = os.path.join(SAVE_DIRECTORY, f"{filename}{SAVE_EXTENSION}")
        
        with open(filepath, "rb") as f:
            player = pickle.load(f)
        
        print(f"📂 Game loaded successfully for {player.name}!")
        return player
    
    except Exception as e:
        print(f"❌ Error loading save file: {e}")
        return None


# ==============================
# DELETE FUNCTIONS
# ==============================

def delete_save(filename: str) -> bool:
    """
    Delete a save file
    
    Args:
        filename: Filename without extension
        
    Returns:
        bool: True if deleted successfully
    """
    try:
        filepath = os.path.join(SAVE_DIRECTORY, f"{filename}{SAVE_EXTENSION}")
        
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️  Save file '{filename}' deleted.")
            return True
        else:
            print(f"❌ Save file '{filename}' not found.")
            return False
    
    except Exception as e:
        print(f"❌ Error deleting save file: {e}")
        return False


def list_saves():
    """Display all available save files"""
    saves = get_save_files()
    
    if not saves:
        print("No save files found.")
        return
    
    print("\n" + "=" * 50)
    print("Available Save Files:".center(50))
    print("=" * 50)
    
    for i, save in enumerate(saves, 1):
        print(f"{i}. {save}")
    
    print("=" * 50)