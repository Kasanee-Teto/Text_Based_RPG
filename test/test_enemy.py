import pytest
from Character.Enemy_RPG import Enemy, WolfBoss, OgreBoss, VampireBoss
from Character.Character_RPG import Player

def test_enemy_difficulty_scaling():
    e = Enemy("Goblin", hp=100, attack=10, defense=10, exp_reward=10)
    scaled = e.scale_difficulty(1.5)
    
    # scale_difficulty returns a dict of new stats, doesn't modify in place immediately 
    # (based on standard implementation, or check if your implementation modifies self)
    # *Correction*: In the provided Enemy_RPG.py, scale_difficulty returns a dict.
    assert scaled['hp'] == 150
    assert scaled['attack'] == 15
    assert scaled['defense'] == 15

def test_enemy_defeated_adds_exp():
    e = Enemy("Test Enemy", hp=10, attack=1, defense=0, exp_reward=7)
    p = Player("Hero")
    e.defeated(p)
    assert p.exp == 7
    assert e.defeated_count == 1

def test_wolf_attack_applies_bleeding():
    wolf = WolfBoss()
    p = Player("Hero")
    wolf.attack(p)
    assert "bleeding" in p.status_effects

def test_vampire_attack_drains_life():
    vamp = VampireBoss()
    p = Player("Hero", start_hp=100, start_attack=5, start_defense=0)
    base_hp = vamp.hp
    vamp.attack(p)
    assert vamp.hp >= base_hp 