import pytest

from Character.Role import (
    Warrior,
    Mage,
    Archer,
    Assassin,
    Healer,
)
from Character.Character_RPG import Player


def _base_stats():
    p = Player("Hero")
    return p, p.attack_power, p.defense, p.hp, p.max_hp


def test_warrior_strategy_applies_bonus():
    p, atk, df, hp, max_hp = _base_stats()
    role = Warrior()
    role.apply_bonus(p)
    assert p.attack_power == atk + 3
    assert p.defense == df + 5
    assert p.hp == hp + 30


def test_mage_strategy_applies_bonus():
    p, atk, df, hp, max_hp = _base_stats()
    role = Mage()
    role.apply_bonus(p)
    assert p.attack_power == atk + 10
    assert p.defense == df - 2


def test_archer_strategy_applies_bonus():
    p, atk, df, hp, max_hp = _base_stats()
    role = Archer()
    role.apply_bonus(p)
    assert p.attack_power == atk + 7
    assert p.defense == df + 2
    assert p.hp == hp + 10


def test_assassin_strategy_applies_bonus_and_crit_rate():
    p, atk, df, hp, max_hp = _base_stats()
    # Tambah atribut kritikal dulu karena Player belum punya
    p.crit_rate = 0.0
    role = Assassin()
    role.apply_bonus(p)
    assert p.attack_power == atk + 12
    assert p.defense == df - 3
    assert p.hp == hp + 5
    assert p.crit_rate == pytest.approx(0.15, rel=1e-6)


def test_healer_strategy_applies_bonus_and_heal():
    p, atk, df, hp, max_hp = _base_stats()
    role = Healer()
    role.apply_bonus(p)
    assert p.attack_power == atk + 2
    assert p.defense == df + 3
    assert p.hp == hp + 15

    # Uji fungsi heal
    target = Player("Target")
    target.take_damage(30)  # reduce HP
    before = target.hp
    role.heal(target)
    assert target.hp == before + 20