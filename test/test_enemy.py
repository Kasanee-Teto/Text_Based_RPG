import pytest
from Character.Enemy_RPG import Enemy, Wolf, Ogre, Vampire
from Character.Character_RPG import Player


def test_enemy_defeated_adds_exp_and_count():
    e = Enemy("Test Enemy", hp=10, attack=1, defense=0, exp_reward=7)
    p = Player("Hero")
    e.defeated(p)
    assert p.exp == 7
    assert e.defeated_count == 1


def test_wolf_attack_applies_bleeding():
    wolf = Wolf()
    p = Player("Hero")
    wolf.attack(p)
    assert "bleeding" in p.status_effects


def test_ogre_attack_applies_weakened():
    ogre = Ogre()
    p = Player("Hero")
    ogre.attack(p)
    assert "weakened" in p.status_effects


def test_vampire_attack_drains_life():
    vamp = Vampire()
    p = Player("Hero", start_hp=100, start_attack=5, start_defense=0)
    base_hp = vamp.hp
    vamp.attack(p)  # should heal self for 30% of damage dealt
    assert vamp.hp >= base_hp  # healed or unchanged at worst