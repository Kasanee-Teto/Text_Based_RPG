import os, pickle

save_game = "save"
os.makedirs(save_game, exist_ok=True)

def save_games (player):
    filename = os.path.join(save_game, f"{player.name}.pkl")
    with open(filename, "wb") as f :
        pickle.dump (player, f)
    print(f"Game for {player.name} saved successfully!")

def load_game():
    files = os.listdir(save_game)
    saves = [f for f in files if f.endswith(".pkl")]
    if not saves:
        print("No saved games found")
        return None
    
    print("Choose a save file:")
    for i, s in enumerate(saves, 1):
        print(f"{i}. {s.replace('.pkl', '')}")

    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(saves):
            filename = os.path.join(save_game, saves[choice-1])
            with open(filename, "rb") as f:
                player = pickle.load(f)
            print(f"Game for {player.name} loaded successfully!")
            return player
        else:
            print("Invalid choice!")
            return None
    except ValueError:
        print("Invalid input!")
        return None