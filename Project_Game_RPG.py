from character import Character

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


class Enemy(Character):
    def __init__(self, name, hp, attack, defense, exp_reward):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward
        self.defeated = 0

    def scale_difficulty(self):
        factor = 1 + (0.2 * self.defeated)
        scaled_hp = int(self.hp * factor)
        scaled_attack = int(self.attack_power * factor)
        scaled_defense = int(self.defense * factor)
        return {"hp": scaled_hp, "attack": scaled_attack, "defense": scaled_defense}

    def mark_defeated(self):
        self.defeated += 1
        print(f"{self.name} telah dikalahkan {self.defeated} kali, jadi lebih kuat!")


# --- SUBCLASS ENEMY SPESIAL ---
class Goblin(Enemy):
    def attack(self, target):
        super().attack(target)

class Wolf(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"{target.name} terkena bleeding!")


class Ogre(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("weakened")
        print(f"{target.name} stat turun sementara (weakened)!")


class Vampire(Enemy):
    def attack(self, target):
        super().attack(target)
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name} menyedot darah! HP pulih {heal}.")


class Demon(Enemy):
    def attack(self, target):
        super().attack(target)
        target.status_effects.append("bleeding")
        print(f"{target.name} terkena bleeding!")
        target.status_effects.append("weakened")
        print(f"{target.name} stat turun sementara (weakened)!")
        heal = int(self.attack_power * 0.3)
        self.hp += heal
        print(f"{self.name} menyedot d arah! HP pulih {heal}.")

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
