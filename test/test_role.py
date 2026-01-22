from Character.Role import Warrior
from Character.Character_RPG import Player


def test_warrior_strategy_applies_bonus():
    p = Player("Hero")
    base_atk, base_def, base_hp = p.attack_power, p.defense, p.hp
    role = Warrior()
    role.apply_bonus(p)
    assert p.attack_power == base_atk + 3
    assert p.defense == base_def + 5
    assert p.hp == base_hp + 30