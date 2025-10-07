[EN](README.md) | ID | [CN](docs/README_CN.md)

# 🎮 RPG Berbasis Teks

Sebuah proyek sekolah sederhana yang dibuat dengan cinta

## 👀 Tinjauan
Proyek ini adalah RPG berbasis teks sederhana yang menggunakan konsep Pemrograman Berbasis Objek (PBO/OOP). Pemain dapat membuat karakter, mengelola inventaris, dan terlibat dalam pertempuran dengan berbagai peran dan item.

## 🪶 Fitur
- Pembuatan karakter dengan atribut yang dapat disesuaikan (nama, poin kesehatan, kekuatan serangan, pertahanan).
- Pemilihan peran untuk karakter (misalnya, Warrior, Mage).
- Sistem inventaris untuk mengelola item (menambah, menghapus, dan melihat daftar item).
- Mekanisme pertarungan dasar di mana karakter dapat saling serang.

## 🏛️ Arsitektur & Diagram Kelas
Proyek ini mengikuti desain Berbasis Objek. Inti dari arsitektur ini melibatkan kelas dasar `Character`, yang dispesialisasikan menjadi kelas `Player`. Pemain mengelola `Inventory` dan dapat diberi `Role`. `Items` juga disusun menggunakan pewarisan.

```mermaid
classDiagram
    class Character {
        -name: str
        -hp: int
        -atk: int
        -defense: int
        +attack(target)
        +is_alive()
    }

    class Player {
        -level: int
        -role: Role
        -inventory: Inventory
        +choose_role(role)
        +use_item(item)
    }

    class Role {
        <<Abstract>>
        -name: str
        +apply_bonus(character)
    }
    
    class Warrior {
      +apply_bonus(character)
    }

    class Mage {
      +apply_bonus(character)
    }

    class Inventory {
        -items: list~Items~
        +add_item(item)
        +remove_item(item)
    }

    class Items {
        <<Abstract>>
        -name: str
        -value: int
    }

    class Weapon {
        -damage: int
    }

    class Armor {
        -defense: int
    }

    Character <|-- Player
    Player "1" o-- "1" Role
    Player "1" o-- "1" Inventory
    Inventory "1" o-- "0..*" Items

    Items <|-- Weapon
    Items <|-- Armor
    
    Role <|-- Warrior
    Role <|-- Mage
```

## 📂 Struktur Proyek
```
text_based_rpg
├── main.py              # Titik masuk aplikasi
├── character            # Modul untuk kelas-kelas terkait karakter
│   ├── __init__.py
│   ├── character.py     # Definisi kelas Character
│   └── role.py          # Definisi kelas Role
├── inventory.py         # Definisi kelas Inventory
├── items.py             # Definisi kelas Items
└── README.md            # Dokumentasi proyek
```

## 👨‍💻 Instruksi Pengaturan
1. *Clone* repositori ini ke mesin lokal Anda.
2. Arahkan ke direktori proyek.
3. Jalankan game dengan mengeksekusi:
   ```
   python main.py
   ```

## 🕹️ Mekanisme Gameplay
- Pemain dapat membuat karakter dan memilih peran setelah mencapai level 5.
- Karakter dapat terlibat dalam pertarungan, bergiliran untuk saling menyerang.
- Pemain dapat mengelola inventaris mereka untuk melengkapi item yang meningkatkan kemampuan mereka.

## 👤 Kontributor

<table border="0" cellspacing="10" cellpadding="5">
  <tr>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/Kasanee-Teto">
        <img src="https://github.com/Kasanee-Teto.png" width="100" height="100" alt="Kasanee-Teto" style="border-radius: 50%;"/>
      </a>
      <br/>
      <a href="https://github.com/Kasanee-Teto">Kasanee-Teto</a>
    </td>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/Solynixx">
        <img src="https://github.com/Solynixx.png" width="100" height="100" alt="Solynixx" style="border-radius: 50%;"/>
      </a>
      <br/>
      <a href="https://github.com/Solynixx">Solynixx</a>
    </td>
    <td align="center" style="border: 1px solid #555; padding: 10px;">
      <a href="https://github.com/Milkdrinker-creator">
        <img src="https://github.com/Milkdrinker-creator.png" width="100" height="100" alt="Milkdrinker-creator" style="border-radius: 50%;"/>
      </a>
      <br/>
      <a href="https://github.com/Milkdrinker-creator">Milkdrinker-creator</a>
    </td>
  </tr>
</table>