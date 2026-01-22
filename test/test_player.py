import pytest

from Character.Character_RPG import Player


class DummyRole:
    def __init__(self, name="Warrior", atk=2, df=3, hp=10):
        self.__class__.__name__ = name
        self.bonus_attack = atk
        self.bonus_defense = df
        self.bonus_hp = hp

    def apply_bonus(self, player: Player):
        player.attack_power += self.bonus_attack
        player.defense += self.bonus_defense
        player.max_hp += self.bonus_hp
        player.hp += self.bonus_hp


class DummyWeapon:
    def __init__(self, name="Sword", damage=5):
        self.name = name
        self.damage = damage


class DummyArmor:
    def __init__(self, name="Shield", defense=4):
        self.name = name
        self.defense = defense


def test_level_up_increases_stats_and_exp_rollover():
    p = Player("Hero", start_hp=100, start_attack=8, start_defense=2, start_coins=0)
    p.gain_exp(100)  # exactly enough
    assert p.level == 2
    assert p.max_hp == 120
    assert p.hp == 120  # healed on level up
    assert p.attack_power == 13
    assert p.defense == 4
    assert p.exp < p.exp_needed  # exp rolled over


def test_choose_role_applies_bonus():
    p = Player("Hero")
    p.level = 5  # simulate requirement met
    role = DummyRole(name="Warrior", atk=3, df=2, hp=15)
    p.choose_role(role)
    assert p.role is role
    assert p.attack_power == 8 + 3
    assert p.defense == 2 + 2
    assert p.max_hp == 100 + 15
    assert p.hp == 100 + 15


def test_equip_weapon_and_swap():
    p = Player("Hero")
    sword = DummyWeapon("Sword", 5)
    axe = DummyWeapon("Axe", 7)
    p.inventory.add_item(sword)
    p.inventory.add_item(axe)

    p.equip_weapon(sword)
    assert p.equipped_weapon is sword
    assert p.attack_power == 8 + 5
    assert sword not in p.inventory.items

    p.equip_weapon(axe)
    assert p.equipped_weapon is axe
    assert p.attack_power == 8 + 7  # swapped damage applied
    assert sword in p.inventory.items


def test_equip_armor_and_swap():
    p = Player("Hero")
    shield = DummyArmor("Shield", 4)
    mail = DummyArmor("Mail", 6)
    p.inventory.add_item(shield)
    p.inventory.add_item(mail)

    p.equip_armor(shield)
    assert p.equipped_armor is shield
    assert p.defense == 2 + 4
    assert shield not in p.inventory.items

    p.equip_armor(mail)
    assert p.equipped_armor is mail
    assert p.defense == 2 + 6
    assert shield in p.inventory.items


def test_status_effects_bleeding_and_weakened():
    p = Player("Hero")
    p.status_effects = ["bleeding", "weakened"]
    p.attack_power = 10
    p.defense = 5
    p.hp = 50

    p.update_status_effects()

    # bleed applies
    assert p.hp == 47
    # weakened applies 20%
    assert p.attack_power == max(1, int(10 * 0.8))
    assert p.defense == max(1, int(5 * 0.8))

    # ensure restoration on next tick when status cleared
    p.status_effects = []
    p.update_status_effects()
    assert p.attack_power == 10
    assert p.defense == 5