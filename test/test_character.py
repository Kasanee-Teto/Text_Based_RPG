import pytest

from Character.Character_RPG import Character


def test_is_alive_and_take_damage():
    c = Character("Goblin", hp=10, attack=3, defense=1)
    assert c.is_alive() is True
    c.take_damage(5)
    assert c.hp == 5
    assert c.is_alive() is True
    c.take_damage(10)  # overkill
    assert c.hp == 0
    assert c.is_alive() is False


def test_attack_uses_defense_and_min_zero():
    attacker = Character("Orc", hp=20, attack=5, defense=1)
    defender = Character("Guard", hp=15, attack=2, defense=10)
    dmg = attacker.attack(defender)
    assert dmg == 0
    assert defender.hp == 15

    defender2 = Character("Peasant", hp=8, attack=1, defense=2)
    dmg2 = attacker.attack(defender2)
    assert dmg2 == 3  # 5 - 2
    assert defender2.hp == 5