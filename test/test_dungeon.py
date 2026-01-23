import pytest
from typing import Any, List, Optional, Dict

from dungeon import Dungeon, Room, DungeonPresenter, SpawnStrategy, RoomEventType
from Character.Character_RPG import Player
from items import Item

# ==============================
# MOCKS FOR DEPENDENCY INJECTION
# ==============================

class MockPresenter:
    def __init__(self):
        self.messages = []
        self.input_queue = []

    def show_entrance_msg(self, depth: int): self.messages.append("entrance")
    def show_exit_msg(self, reward: int): self.messages.append("exit_unlocked")
    def show_room(self, desc, summary, map_str, x, y, has_key): self.messages.append("show_room")
    def show_trap_trigger(self, name, damage, player, status): self.messages.append("trap")
    def show_combat_start(self, name): self.messages.append("combat")
    def show_treasure_found(self, name): self.messages.append("treasure")
    def show_retreat_msg(self): self.messages.append("retreat")
    def show_key_found(self): self.messages.append("key_found")
    def show_exit_locked(self): self.messages.append("exit_locked")
    def show_game_complete(self): self.messages.append("game_complete")
    
    def get_movement_input(self, available_moves: List[str]) -> Optional[str]:
        if self.input_queue: return self.input_queue.pop(0)
        return 'q'

class MockSpawner:
    def create_enemy(self, depth: int) -> Any:
        class DummyEnemy:
            def __init__(self): 
                self.name = "Dummy"
                self.max_hp = 10
                self.hp = 10
                self.attack_power = 1
                self.defense = 0
            def scale_difficulty(self, f): pass
            def is_alive(self): return self.hp > 0
            def attack(self, target): pass
            def defeated(self, player): pass
        return DummyEnemy()

    def create_boss(self, depth: int) -> Any: return self.create_enemy(depth)
    def create_final_boss(self, depth: int) -> Any: return self.create_enemy(depth)
    
    def create_loot(self) -> Item:
        class DummyItem:
            def __init__(self): 
                self.name = "Gold"
                self.value = 10
        return DummyItem()

    def create_trap(self) -> Dict[str, Any]:
        return {"name": "Test Trap", "damage": 5, "status": None}

# ==============================
# TESTS
# ==============================

def test_dungeon_initialization_and_scaling():
    # Depth 1 should be small
    d1 = Dungeon(MockSpawner(), MockPresenter(), depth=1, seed=42)
    assert d1.width <= 15
    assert d1.height <= 15
    assert d1.player_has_key is False

    # Depth 20 should be maxed (15x15)
    d20 = Dungeon(MockSpawner(), MockPresenter(), depth=20, seed=42)
    assert d20.width == 15
    assert d20.height == 15

def test_key_and_exit_placement():
    d = Dungeon(MockSpawner(), MockPresenter(), depth=1, seed=123)
    
    entrance_room = d.get_room(*d.start_pos)
    assert entrance_room.is_entrance is True
    
    exit_room = d.get_room(*d.exit_pos)
    assert exit_room.is_exit is True
    
    # Verify key exists somewhere in the map or on player
    key_in_room = any(r.has_key for row in d.map for r in row)
    assert key_in_room or d.player_has_key

def test_exit_locked_mechanic():
    presenter = MockPresenter()
    d = Dungeon(MockSpawner(), presenter, depth=1, seed=1)
    p = Player("Tester")
    
    # Ensure player doesn't have key
    d.player_has_key = False
    
    # Try to exit
    success = d._handle_exit(p)
    assert success is False
    assert "exit_locked" in presenter.messages

def test_exit_unlocked_mechanic():
    presenter = MockPresenter()
    d = Dungeon(MockSpawner(), presenter, depth=1, seed=1)
    p = Player("Tester")
    
    # Give key
    d.player_has_key = True
    
    # Try to exit
    success = d._handle_exit(p)
    assert success is True
    assert "exit_unlocked" in presenter.messages
    assert p.coins > 200 # Should have gained reward

def test_explore_finds_key():
    presenter = MockPresenter()
    d = Dungeon(MockSpawner(), presenter, depth=1, seed=1)
    p = Player("Tester")
    
    # Find room with key
    key_x, key_y = -1, -1
    for row in d.map:
        for r in row:
            if r.has_key:
                key_x, key_y = r.x, r.y
                break
    
    # If key wasn't auto-given (map size check), verify picking it up
    if key_x != -1:
        d.player_has_key = False # Reset just in case
        d.start_pos = (key_x, key_y) # Teleport start to key
        presenter.input_queue = ['q'] # Quit immediately after start
        
        d.explore_from(p, lambda pl, en: None)
        assert d.player_has_key is True
        assert "key_found" in presenter.messages

def test_handle_trap_scaling():
    spawner = MockSpawner()
    presenter = MockPresenter()
    d = Dungeon(spawner, presenter, depth=10, seed=1) # Depth 10
    
    p = Player("Tester", start_hp=100)
    room = d.get_room(0, 0)
    room.trap = {"name": "Spike", "damage": 10, "status": None}
    
    d._handle_trap(room, p)
    
    # Base damage 10. Depth 10 adds 100% (1 + 10*0.1 = 2.0x multiplier) -> 20 damage
    assert p.hp == 80 
    assert "trap" in presenter.messages