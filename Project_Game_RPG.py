from character import Character
from Enemy_RPG import Demon , Vampire . Orge , Wolf , Goblin

class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=15, defense=10)
        self.exp = 0
        self.level = 1
        self.status_effects = [] 

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.attack_power += 5
        self.defense += 2
        print(f"{self.name} naik level! Sekarang level {self.level}.")


#Menu
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


#Program
if __name__ == "__main__":
    main()



