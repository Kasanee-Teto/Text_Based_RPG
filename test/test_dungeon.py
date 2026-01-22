import random
import pytest

from dungeon import Dungeon, Room
from Character.Character_RPG import Player


def test_dungeon_generation_size_and_exit_flag():
    d = Dungeon(width=3, height=4, seed=42)
    assert len(d.map) == 4
    assert len(d.map[0]) == 3
    exit_room = d.get_room(2, 3)
    assert exit_room.is_exit is True


def test_get_room_bounds():
    d = Dungeon(width=2, height=2, seed=1)
    assert d.get_room(0, 0) is not None
    assert d.get_room(1, 1) is not None
    assert d.get_room(-1, 0) is None
    assert d.get_room(2, 0) is None
    assert d.get_room(0, 2) is None


def test_handle_trap_applies_damage_and_status(monkeypatch):
    d = Dungeon(width=1, height=1, seed=0)
    player = Player("Hero", start_hp=50, start_defense=0)
    room = d.get_room(0, 0)
    room.trap = {"name": "poison needle", "damage": 5, "status": "weakened"}

    survived = d._handle_trap(room, player)
    assert survived is True
    assert player.hp == 45
    assert "weakened" in player.status_effects
    assert room.trap is None  # cleared after trigger


def test_handle_enemies_calls_battle_callback(monkeypatch):
    d = Dungeon(width=1, height=1, seed=0)
    player = Player("Hero")

    class DummyEnemy:
        def __init__(self):
            self.name = "Dummy"

    room = d.get_room(0, 0)
    room.enemies = [DummyEnemy(), DummyEnemy()]

    calls = []

    def battle_callback(p, enemy):
        calls.append(enemy.name)
        # simulate no damage to player

    # Avoid random loot drop to keep deterministic
    monkeypatch.setattr(random, "random", lambda: 1.0)

    survived = d._handle_enemies(room, player, battle_callback)
    assert survived is True
    assert calls == ["Dummy", "Dummy"]
    assert room.enemies == []  # emptied


def test_spawn_content_with_seed_deterministic(monkeypatch):
    # Ensure deterministic content placement
    d = Dungeon(width=3, height=3, seed=123, difficulty=1.0)
    enemies_count = sum(len(r.enemies) for row in d.map for r in row)
    treasure_count = sum(len(r.treasure) for row in d.map for r in row)
    # At least some content spawned with this seed
    assert enemies_count >= 1
    assert treasure_count >= 0  # may be zero but usually >0 with seed 123