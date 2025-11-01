
import random
from Character.Enemy_RPG import goblin, spider, skeleton, zombie, Wolf, Ogre, Vampire, Demon
from items import Small_HPotion, Medium_HPotion, Short_Sword, Short_bow, Wizards_Robe, Leather_Armor
from inventory import Inventory

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.is_exit = False
        self.enemies = []      # list of Enemy instances
        self.treasure = []     # list of item objects
        self.trap = None       # trap dict or None
        self.description = "An empty, damp room."

    def has_danger(self):
        return bool(self.enemies) or self.trap is not None

    def summary(self):
        parts = []
        if self.enemies:
            parts.append(f"Enemies: {', '.join([e.name for e in self.enemies])}")
        if self.treasure:
            parts.append(f"Treasure: {', '.join([t.name for t in self.treasure])}")
        if self.trap:
            parts.append(f"Trap: {self.trap['name']}")
        if not parts:
            parts.append("Nothing here.")
        return " | ".join(parts)


class Dungeon:
    def __init__(self, width=5, height=5, depth=1, seed=None, difficulty=1.0):
        """
        width, height : grid size of rooms
        depth : dungeon floor (affects enemy scaling)
        seed : optional int for reproducible dungeons
        difficulty : multiplier for enemy count / strength
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.seed = seed
        self.difficulty = difficulty
        if seed is not None:
            random.seed(seed)
        self.map = self._generate_map()
        self.start = (0, 0)
        self.exit = (width - 1, height - 1)
        self.map[self.exit[1]][self.exit[0]].is_exit = True

    def _generate_map(self):
        grid = [[Room(x, y) for x in range(self.width)] for y in range(self.height)]
        # Fill rooms with content based on probability and difficulty
        for y in range(self.height):
            for x in range(self.width):
                room = grid[y][x]
                # Slightly nicer descriptions
                descs = [
                    "a damp stone chamber",
                    "a narrow corridor",
                    "a collapsed hall",
                    "a room lit by bioluminescent moss",
                    "a cavern with dripping water"
                ]
                room.description = "You see " + random.choice(descs) + "."

                # Randomly place enemies (based on difficulty)
                if random.random() < 0.45 * self.difficulty:
                    # choose enemy type by difficulty / depth
                    enemy_choice = random.random()
                    if self.depth >= 3 and random.random() < 0.15:
                        room.enemies.append(Demon())
                    elif enemy_choice < 0.3:
                        room.enemies.append(spider())
                    elif enemy_choice < 0.6:
                        room.enemies.append(goblin())
                    elif enemy_choice < 0.85:
                        room.enemies.append(skeleton())
                    else:
                        room.enemies.append(zombie())

                # Boss rooms (rare) near bottom-right with small chance
                if (x, y) == (self.width-1, self.height-2) and random.random() < 0.25:
                    room.enemies.append(Wolf())

                # Random treasure
                if random.random() < 0.25:
                    loot = random.choice([Small_HPotion, Medium_HPotion, Short_Sword, Short_bow, Wizards_Robe, Leather_Armor])
                    room.treasure.append(loot)

                # Traps
                if random.random() < 0.10:
                    trap = random.choice([
                        {"name": "spike trap", "damage": 8},
                        {"name": "poison needle", "damage": 5, "status": "weakened"},
                    ])
                    room.trap = trap

        # Entrance: ensure some content at start or not, up to you
        grid[0][0].description = "Dungeon entrance: cold stones and the smell of decay."
        return grid

    def display_map(self, player_pos=None, reveal_visited=False):
        """
        ASCII-mini-map: P for player, E for exit, ? for unknown (if not visited), . for empty visited, M for monster, T for treasure.
        """
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                r = self.map[y][x]
                if player_pos == (x, y):
                    row.append("P")
                elif r.is_exit:
                    row.append("E")
                elif not reveal_visited and not r.visited:
                    row.append("?")
                else:
                    # prioritize marking monsters/treasure for visited rooms
                    if r.enemies:
                        row.append("M")
                    elif r.treasure:
                        row.append("T")
                    else:
                        row.append(".")
                # optional: color could be added if terminal supports it
            rows.append(" ".join(row))
        print("\n".join(rows))

    def get_room(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x]
        return None

    def explore_from(self, player, battle_callback):
        """
        Main interactive exploration loop for the dungeon.
        - player: your Player instance
        - battle_callback: function(player, enemy) -> uses your existing battle logic
        Returns after player leaves or dies.
        """
        x, y = self.start
        current_room = self.get_room(x, y)
        current_room.visited = True
        print("You step into the dungeon...")

        while True:
            print("\n--- Dungeon Map ---")
            self.display_map(player_pos=(x, y), reveal_visited=True)
            room = self.get_room(x, y)
            print(f"\nYou are at ({x},{y}): {room.description}")
            print("Room summary:", room.summary())
            # If trap and not disarmed earlier
            if room.trap:
                trap = room.trap
                print(f"Trap triggered: {trap['name']}!")
                dmg = trap.get("damage", 0)
                if dmg:
                    player.take_damage(dmg)
                    print(f"{player.name} took {dmg} damage from trap. HP: {player.hp}/{player.max_hp}")
                    if not player.is_alive():
                        print("You died to a trap...")
                        return False  # player died
                # apply status optionally
                if trap.get("status"):
                    player.status_effects.append(trap["status"])
                    print(f"{player.name} is afflicted with {trap['status']}.")

                # trap triggers only once
                room.trap = None

            # If enemies exist -> fight them one by one
            if room.enemies:
                # iterate shallow copy because battle may modify enemy.hp
                while room.enemies and player.is_alive():
                    enemy = room.enemies.pop(0)
                    print(f"\nAn enemy appears: {enemy.name}!")
                    # call the existing battle function
                    battle_callback(player, enemy)
                    if not player.is_alive():
                        print("You were defeated in the dungeon...")
                        return False
                    # On enemy defeat: give loot directly (small chance) and exp already handled by enemy.defeated
                    # The enemy.defeated in Enemy_RPG.py already awards exp; we can drop items here:
                    if random.random() < 0.5:
                        loot = random.choice([Small_HPotion, Medium_HPotion, Short_Sword, Short_bow, Wizards_Robe, Leather_Armor])
                        player.inventory.add_item(loot)
                        print(f"Found loot on the enemy: {loot.name}")

            # If treasure in room, take automatically (or you can prompt)
            if room.treasure:
                for item in room.treasure:
                    player.inventory.add_item(item)
                    print(f"You discovered treasure: {item.name}")
                room.treasure = []

            # If this is the exit
            if room.is_exit:
                print("You found the exit of this level!")
                # optionally give floor reward
                floor_reward = int(50 * self.difficulty + 10 * self.depth)
                player.coins += floor_reward
                print(f"You collect {floor_reward} coins at the exit. Total coins: {player.coins}")
                return True

            # Movement choices
            moves = {}
            if self.get_room(x, y-1): moves['n'] = (x, y-1)
            if self.get_room(x, y+1): moves['s'] = (x, y+1)
            if self.get_room(x-1, y): moves['w'] = (x-1, y)
            if self.get_room(x+1, y): moves['e'] = (x+1, y)
            print("\nMoves available:", ", ".join([k.upper() for k in moves.keys()]) + " | (Q)uit dungeon and leave")
            choice = input("Move (N/S/E/W) or Q to quit: ").strip().lower()
            if choice == 'q':
                print("You retreat from the dungeon.")
                return True
            if choice in moves:
                x, y = moves[choice]
                self.get_room(x, y).visited = True
                continue
            else:
                print("Invalid move. Try again.")
