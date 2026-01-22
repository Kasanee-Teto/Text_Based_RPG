import pytest

from items import Weapon, Armor, HealthPotion
from Character.Character_RPG import Character


class DummyChar(Character):
    def __init__(self):
        super().__init__("Hero", hp=50, attack=5, defense=2)


def test_weapon_attributes():
    w = Weapon("Short Sword", weapon_type="Sharp", damage=7, value=25, rarity="Uncommon")
    assert w.name == "Short Sword"
    assert w.weapon_type == "Sharp"
    assert w.damage == 7
    assert w.value == 25
    assert w.rarity == "Uncommon"
    assert "Weapon" in repr(w)


def test_armor_attributes():
    a = Armor("Leather Armor", defense=3, defense_type="Blunt", value=20, rarity="Common")
    assert a.name == "Leather Armor"
    assert a.defense == 3
    assert a.defense_type == "Blunt"
    assert a.value == 20
    assert a.rarity == "Common"
    assert "Armor" in repr(a)


def test_health_potion_uses_heals_up_to_max_hp():
    p = DummyChar()
    potion = HealthPotion("Small Potion", value=5, heals=15)
    p.take_damage(20)  # hp -> 30
    potion.uses(p)
    assert p.hp == 45  # 30 + 15, under max
    potion.uses(p)
    assert p.hp == p.max_hp  # capped at max_hp