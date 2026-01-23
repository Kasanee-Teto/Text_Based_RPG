import os
import pickle
import pytest
import save_game_RPG as sg
from Character.Character_RPG import Player

def test_save_and_load_includes_depth(tmp_path, monkeypatch):
    save_dir = tmp_path / "saves"
    monkeypatch.setattr(sg, "SAVE_DIRECTORY", save_dir)
    os.makedirs(save_dir, exist_ok=True)

    player = Player("Explorer")
    player.current_depth = 5 # Set custom depth
    
    sg.save_game(player, custom_filename="slot_depth")

    loaded = sg.load_game(filename="slot_depth")
    assert isinstance(loaded, Player)
    assert loaded.name == "Explorer"
    assert loaded.current_depth == 5

def test_delete_save(tmp_path, monkeypatch):
    save_dir = tmp_path / "saves"
    monkeypatch.setattr(sg, "SAVE_DIRECTORY", save_dir)
    os.makedirs(save_dir, exist_ok=True)

    file_path = save_dir / "slot2.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(Player("Tester"), f)

    assert sg.delete_save("slot2") is True
    assert not file_path.exists()