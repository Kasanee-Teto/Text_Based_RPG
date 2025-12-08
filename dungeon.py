"""
Dungeon generation and exploration system
Procedurally generates dungeons with rooms, enemies, treasure, and traps
"""

import random
from Character.Enemy_RPG import Goblin_Grunt, Spider, Skeleton, Zombie, Wolf, Ogre, Vampire, Demon
from items import Small_HPotion, Medium_HPotion, Short_Sword, Short_bow, Wizards_Robe, Leather_Armor
from typing import List, Tuple, Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from Character.Character_RPG import Player


# ==============================
# ROOM CLASS
# ==============================

class Room:
    """
    Represents a single room in the dungeon
    
    Attributes:
        x (int): X coordinate in dungeon grid
        y (int): Y coordinate in dungeon grid
        visited (bool): Whether player has been here
        is_exit (bool): Whether this is the exit room
        enemies (List): Enemy instances in this room
        treasure (List): Item objects in this room
        trap (dict): Trap data (name, damage, status effect)
        description (str): Flavor text for the room
    """
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.is_exit = False
        self.enemies: List = []
        self.treasure: List = []
        self.trap: Optional[dict] = None
        self.description = "An empty, damp room."
    
    def has_danger(self) -> bool:
        """Check if room contains enemies or traps"""
        return bool(self.enemies) or self.trap is not None
    
    def has_content(self) -> bool:
        """Check if room has any content"""
        return bool(self.enemies) or bool(self.treasure) or self. trap is not None
    
    def summary(self) -> str:
        """
        Get a text summary of room contents
        
        Returns:
            str: Description of room contents
        """
        parts = []
        if self.enemies:
            enemy_names = ', '.join([e.name for e in self.enemies])
            parts.append(f"⚔️  Enemies: {enemy_names}")
        if self.treasure:
            treasure_names = ', '.join([t. name for t in self.treasure])
            parts.append(f"💎 Treasure: {treasure_names}")
        if self.trap:
            parts.append(f"⚠️  Trap: {self. trap['name']}")
        if not parts:
            parts.append("✓ Nothing here.")
        return " | ".join(parts)
    
    def clear_enemies(self):
        """Remove all enemies from room"""
        self. enemies. clear()
    
    def clear_treasure(self):
        """Remove all treasure from room"""
        self.treasure.clear()


# ==============================
# DUNGEON CLASS
# ==============================

class Dungeon:
    """
    Procedurally generated dungeon with grid-based rooms
    
    Attributes:
        width (int): Number of rooms horizontally
        height (int): Number of rooms vertically
        depth (int): Dungeon floor level (affects difficulty)
        seed (int): Random seed for reproducible generation
        difficulty (float): Difficulty multiplier
        map (List[List[Room]]): 2D grid of Room objects
        start (Tuple[int, int]): Starting coordinates
        exit (Tuple[int, int]): Exit coordinates
    """
    
    def __init__(self, width: int = 5, height: int = 5, depth: int = 1, 
                 seed: Optional[int] = None, difficulty: float = 1.0):
        """
        Initialize and generate a dungeon
        
        Args:
            width: Horizontal room count
            height: Vertical room count
            depth: Floor level (affects enemy scaling)
            seed: Random seed for generation
            difficulty: Spawn rate and enemy strength multiplier
        """
        self. width = width
        self.height = height
        self.depth = depth
        self.seed = seed
        self.difficulty = difficulty
        
        if seed is not None:
            random.seed(seed)
        
        self.map: List[List[Room]] = self._generate_map()
        self.start: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (width - 1, height - 1)
        self.map[self.exit[1]][self.exit[0]].is_exit = True
    
    def _generate_map(self) -> List[List[Room]]:
        """
        Generate the dungeon grid with rooms and content
        
        Returns:
            List[List[Room]]: 2D grid of rooms
        """
        grid = [[Room(x, y) for x in range(self.width)] for y in range(self. height)]
        
        # Populate rooms with content
        for y in range(self.height):
            for x in range(self.width):
                room = grid[y][x]
                self._generate_room_description(room)
                self._spawn_enemies(room)
                self._spawn_treasure(room)
                self._spawn_traps(room)
        
        # Special entrance room
        grid[0][0].description = "Dungeon entrance: cold stones and the smell of decay."
        
        return grid
    
    def _generate_room_description(self, room: Room):
        """Generate atmospheric description for a room"""
        descriptions = [
            "a damp stone chamber",
            "a narrow corridor",
            "a collapsed hall",
            "a room lit by bioluminescent moss",
            "a cavern with dripping water",
            "an ancient throne room",
            "a forgotten library",
            "a torture chamber with rusty chains",
            "a spiral staircase landing"
        ]
        room.description = "You see " + random.choice(descriptions) + "."
    
    def _spawn_enemies(self, room: Room):
        """
        Randomly spawn enemies in a room based on difficulty
        
        Args:
            room: Room to populate
        """
        # Skip spawn sometimes
        if random.random() > 0.45 * self.difficulty:
            return
        
        # Choose enemy type based on depth
        enemy_choice = random.random()
        
        # Rare demon spawn on deep floors
        if self.depth >= 3 and random.random() < 0.15:
            room.enemies.append(Demon())
        elif enemy_choice < 0.3:
            room.enemies.append(Spider)
        elif enemy_choice < 0.6:
            room.enemies.append(Goblin_Grunt)
        elif enemy_choice < 0.85:
            room.enemies.append(Skeleton)
        else:
            room.enemies.append(Zombie)
        
        # Boss spawn near exit
        if (room.x, room.y) == (self. width - 1, self.height - 2):
            if random.random() < 0.25:
                boss_choice = random.choice([Wolf(), Ogre(), Vampire()])
                room.enemies.append(boss_choice)
    
    def _spawn_treasure(self, room: Room):
        """
        Randomly spawn treasure in a room
        
        Args:
            room: Room to populate
        """
        if random.random() < 0.25:
            loot_pool = [
                Small_HPotion, Medium_HPotion,
                Short_Sword, Short_bow,
                Wizards_Robe, Leather_Armor
            ]
            room.treasure.append(random.choice(loot_pool))
    
    def _spawn_traps(self, room: Room):
        """
        Randomly spawn traps in a room
        
        Args:
            room: Room to populate
        """
        if random.random() < 0.10:
            trap_types = [
                {"name": "spike trap", "damage": 8},
                {"name": "poison needle", "damage": 5, "status": "weakened"},
                {"name": "falling rocks", "damage": 12},
                {"name": "flame jet", "damage": 10},
            ]
            room.trap = random.choice(trap_types)
    
    def get_room(self, x: int, y: int) -> Optional[Room]:
        """
        Get room at coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Room if valid coordinates, None otherwise
        """
        if 0 <= x < self. width and 0 <= y < self.height:
            return self.map[y][x]
        return None
    
    def display_map(self, player_pos: Optional[Tuple[int, int]] = None, reveal_visited: bool = False):
        """
        Display ASCII mini-map of dungeon
        
        Legend:
            P = Player position
            E = Exit
            M = Monster room (visited)
            T = Treasure room (visited)
            .  = Empty room (visited)
            ?  = Unknown room (not visited)
        
        Args:
            player_pos: Current player coordinates
            reveal_visited: Show content of visited rooms
        """
        print("\n╔" + "═" * (self. width * 2 - 1) + "╗")
        
        for y in range(self. height):
            row = []
            for x in range(self.width):
                room = self.map[y][x]
                
                if player_pos == (x, y):
                    row.append("P")
                elif room.is_exit:
                    row.append("E")
                elif not reveal_visited or not room.visited:
                    row.append("?")
                else:
                    # Show room content for visited rooms
                    if room. enemies:
                        row.append("M")
                    elif room.treasure:
                        row.append("T")
                    elif room. trap:
                        row.append("!")
                    else:
                        row.append(".")
            
            print("║" + " ". join(row) + "║")
        
        print("╚" + "═" * (self.width * 2 - 1) + "╝")
    
    def explore_from(self, player: 'Player', battle_callback: Callable) -> bool:
        """
        Main exploration loop for the dungeon
        
        Args:
            player: Player character
            battle_callback: Function(player, enemy) for combat
            
        Returns:
            bool: True if player completed/left dungeon, False if died
        """
        x, y = self.start
        current_room = self.get_room(x, y)
        current_room.visited = True
        print("\n" + "=" * 50)
        print("🏰 You step into the dungeon... ". center(50))
        print("=" * 50)
        
        while True:
            print("\n--- Dungeon Map ---")
            self.display_map(player_pos=(x, y), reveal_visited=True)
            
            room = self.get_room(x, y)
            print(f"\n📍 Position: ({x},{y})")
            print(f"   {room.description}")
            print(f"   {room.summary()}")
            
            # Handle traps
            if room.trap:
                if not self._handle_trap(room, player):
                    return False  # Player died to trap
            
            # Handle enemies
            if room.enemies:
                if not self._handle_enemies(room, player, battle_callback):
                    return False  # Player died in combat
            
            # Handle treasure
            if room.treasure:
                self._handle_treasure(room, player)
            
            # Check if exit
            if room.is_exit:
                return self._handle_exit(player)
            
            # Movement
            if not self._handle_movement(player):
                break  # Player chose to leave
            
            # Update position
            next_pos = self._get_next_position(x, y)
            if next_pos:
                x, y = next_pos
                self.get_room(x, y).visited = True
        
        print("🚪 You retreat from the dungeon.")
        return True
    
    def _handle_trap(self, room: Room, player: 'Player') -> bool:
        """
        Trigger and resolve trap in room
        
        Returns:
            bool: True if player survived, False if died
        """
        trap = room.trap
        print(f"\n⚠️  Trap triggered: {trap['name']}!")
        
        damage = trap. get("damage", 0)
        if damage:
            player.take_damage(damage)
            print(f"💥 {player.name} took {damage} damage!  HP: {player.hp}/{player.max_hp}")
            
            if not player.is_alive():
                print("💀 You died to a trap...")
                return False
        
        # Apply status effect
        if trap.get("status"):
            player.status_effects.append(trap["status"])
            print(f"😵 {player.name} is afflicted with {trap['status']}.")
        
        # Trap triggers only once
        room.trap = None
        return True
    
    def _handle_enemies(self, room: Room, player: 'Player', battle_callback: Callable) -> bool:
        """
        Handle combat with all enemies in room
        
        Returns:
            bool: True if player won, False if died
        """
        while room.enemies and player.is_alive():
            enemy = room.enemies.pop(0)
            print(f"\n⚔️  An enemy appears: {enemy.name}!")
            
            # Use provided battle function
            battle_callback(player, enemy)
            
            if not player.is_alive():
                print("💀 You were defeated in the dungeon...")
                return False
            
            # Random loot drop
            if random.random() < 0.5:
                loot_pool = [Small_HPotion, Medium_HPotion, Short_Sword, Short_bow, Wizards_Robe, Leather_Armor]
                loot = random.choice(loot_pool)
                player.inventory.add_item(loot)
                print(f"🎁 Found loot on the enemy: {loot.name}")
        
        return True
    
    def _handle_treasure(self, room: Room, player: 'Player'):
        """Collect all treasure in room"""
        for item in room.treasure:
            player.inventory.add_item(item)
            print(f"💎 You discovered treasure: {item.name}")
        room.clear_treasure()
    
    def _handle_exit(self, player: 'Player') -> bool:
        """Handle reaching the dungeon exit"""
        print("\n" + "=" * 50)
        print("🎉 You found the exit of this level! ".center(50))
        print("=" * 50)
        
        # Floor completion reward
        floor_reward = int(50 * self.difficulty + 10 * self.depth)
        player.coins += floor_reward
        print(f"💰 You collected {floor_reward} coins at the exit.")
        print(f"   Total coins: {player.coins}")
        
        return True
    
    def _handle_movement(self, player: 'Player') -> bool:
        """
        Display movement options and get player choice
        
        Returns:
            bool: True to continue exploring, False to quit
        """
        # This is a placeholder - actual movement handled in explore_from
        # Kept for potential future refactoring
        return True
    
    def _get_next_position(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """
        Get player's next position from input
        
        Args:
            x: Current X
            y: Current Y
            
        Returns:
            Tuple of new coordinates, or None if invalid/quit
        """
        moves = {}
        if self.get_room(x, y - 1): moves['n'] = (x, y - 1)
        if self.get_room(x, y + 1): moves['s'] = (x, y + 1)
        if self.get_room(x - 1, y): moves['w'] = (x - 1, y)
        if self.get_room(x + 1, y): moves['e'] = (x + 1, y)
        
        print("\n🧭 Available moves:", ", ".join([k. upper() for k in moves.keys()]) + " | (Q)uit dungeon")
        choice = input("➤ Move (N/S/E/W) or Q to quit: ").strip().lower()
        
        if choice == 'q':
            return None
        
        return moves.get(choice, None)
