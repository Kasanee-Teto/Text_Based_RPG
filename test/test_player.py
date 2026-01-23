import pytest
from Character.Character_RPG import Player

class DummyRole:
    def apply_bonus(self, player: Player):
        player.attack_power += 2

class DummyWeapon:
    def __init__(self, name="Sword", damage=5):
        self.name = name
        self.damage = damage
        self.value = 10

def test_level_up_increases_stats():
    p = Player("Hero", start_hp=100)
    p.gain_exp(100)
    assert p.level == 2
    assert p.max_hp == 120

def test_current_depth_initialization():
    p = Player("Hero")
    assert p.current_depth == 1

def test_equip_weapon():
    p = Player("Hero", start_attack=10)
    sword = DummyWeapon("Sword", 5)
    p.inventory.add_item(sword)
    
    p.equip_weapon(sword)
    assert p.attack_power == 15
    assert sword not in p.inventory.items