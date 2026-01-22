import os
import pickle

import pytest

import save_game_RPG as sg
from Character.Character_RPG import Player


def test_save_and_load_game(tmp_path, monkeypatch):
    # isolate save directory
    save_dir = tmp_path / "saves"
    monkeypatch.setattr(sg, "SAVE_DIRECTORY", save_dir)
    os.makedirs(save_dir, exist_ok=True)

    player = Player("Tester")
    ok = sg.save_game(player, custom_filename="slot1")
    assert ok is True

    # file written
    file_path = save_dir / "slot1.pkl"
    assert file_path.exists()

    loaded = sg.load_game(filename="slot1")
    assert isinstance(loaded, Player)
    assert loaded.name == "Tester"


def test_delete_save(tmp_path, monkeypatch):
    save_dir = tmp_path / "saves"
    monkeypatch.setattr(sg, "SAVE_DIRECTORY", save_dir)
    os.makedirs(save_dir, exist_ok=True)

    # create fake save file
    file_path = save_dir / "slot2.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(Player("Tester"), f)

    assert file_path.exists()
    assert sg.delete_save("slot2") is True
    assert not file_path.exists()