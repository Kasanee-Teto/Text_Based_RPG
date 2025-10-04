from character.character import Player
from character.enemy import Goblin, Wolf, Ogre, Vampire, Demon

def menu():
    print("=== MENU RPG SEDERHANA ===")
    print("1. Mulai Game")
    print("2. Keluar")
    pilihan = input("Pilih menu: ")
    return pilihan

def main():
    while True:
        pilihan = menu()
        if pilihan == "1":
            # Buat player
            name = input("Masukkan nama player: ")
            p = Player(name)
        elif pilihan == "2":
            print("Keluar game. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid!\n")

if __name__ == "__main__":
    main()
