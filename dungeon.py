"""
Dungeon generation and exploration system.
"""
import random
from enum import Enum, auto
from typing import List, Tuple, Optional, Callable, Dict, Any

from Character.Character_RPG import Player
from Character.Enemy_RPG import (
    GoblinGrunt, CaveSpider, Skeleton, Zombie, 
    WolfBoss, OgreBoss, VampireBoss, DemonBoss, Enemy
)
from items import (
    SmallHPotion, MediumHPotion, ShortSword, ShortBow, 
    WizardsRobe, LeatherArmor, Item
)
from config import CONFIG

class RoomEventType(Enum):
    EMPTY = auto()
    ENEMY = auto()
    TREASURE = auto()
    TRAP = auto()

class Room:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.is_exit = False
        self.is_entrance = False
        
        self.event_type: RoomEventType = RoomEventType.EMPTY
        self.enemy: Optional[Enemy] = None
        self.treasure: List[Item] = []
        self.trap: Optional[Dict[str, Any]] = None
        
        self.description = "An empty, damp room."
    
    def summary(self) -> str:
        parts = []
        if self.is_entrance:
            parts.append("Start Point")
        
        if self.enemy:
            parts.append(f"⚔️ Enemy: {self.enemy.name}")
        elif self.treasure:
            names = ', '.join([t.name for t in self.treasure])
            parts.append(f"💎 Treasure: {names}")
        elif self.trap:
            parts.append(f"⚠️ Trap: {self.trap['name']}")
            
        if self.is_exit:
            parts.append("🚪 Exit")
            
        if not parts:
            parts.append("✓ Nothing here.")
        return " | ".join(parts)

class Dungeon:
    def __init__(self, width: int = CONFIG.DUNGEON.DEFAULT_WIDTH, 
                 height: int = CONFIG.DUNGEON.DEFAULT_HEIGHT, 
                 depth: int = 1, 
                 seed: Optional[int] = None, 
                 difficulty: float = 1.0):
        self.width = width
        self.height = height
        self.depth = depth
        self.difficulty = difficulty
        
        if seed is not None:
            random.seed(seed)
        
        self.map: List[List[Room]] = self._generate_grid()
        self.start_pos: Tuple[int, int] = (0, 0)
        self.exit_pos: Tuple[int, int] = (width - 1, height - 1)
        
        self._generate_layout()

    def get_room(self, x: int, y: int) -> Optional[Room]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x]
        return None

    def _generate_grid(self) -> List[List[Room]]:
        return [[Room(x, y) for x in range(self.width)] for y in range(self.height)]

    def _generate_layout(self):
        # 1. Place Entrance and Exit
        coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        self.start_pos = random.choice(coords)
        coords.remove(self.start_pos)
        self.exit_pos = random.choice(coords)
        
        # Configure meta flags
        start_room = self.get_room(*self.start_pos)
        start_room.is_entrance = True
        start_room.description = "Dungeon entrance: cold stones and the smell of decay."
        
        exit_room = self.get_room(*self.exit_pos)
        exit_room.is_exit = True
        exit_room.description = "You see a faint light. It might be the exit."
        
        # 2. Fill content for other rooms
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.start_pos:
                    continue
                
                room = self.map[y][x]
                self._generate_room_content(room)
                if not room.is_exit and not room.is_entrance:
                    self._assign_description(room)

    def _generate_room_content(self, room: Room):
        # Logic: Prioritize Boss at Exit > Demon (Rare) > Normal content
        
        # Exit Room Boss Logic
        if room.is_exit:
            if random.random() < CONFIG.DUNGEON.SPAWN_RATE_BOSS:
                self._spawn_boss(room)
            return

        # Rare Demon Logic (Deep floors)
        if self.depth >= 3 and random.random() < CONFIG.DUNGEON.SPAWN_RATE_DEMON:
            room.event_type = RoomEventType.ENEMY
            room.enemy = DemonBoss()
            room.enemy.scale_difficulty(self.difficulty)
            return

        # Standard Roll
        roll = random.random()
        
        # Enemy?
        if roll < CONFIG.DUNGEON.SPAWN_RATE_ENEMY * self.difficulty:
            self._spawn_enemy(room)
        # Treasure?
        elif roll < (CONFIG.DUNGEON.SPAWN_RATE_ENEMY * self.difficulty + 
                     CONFIG.DUNGEON.SPAWN_RATE_TREASURE):
            self._spawn_treasure(room)
        # Trap?
        elif roll < (CONFIG.DUNGEON.SPAWN_RATE_ENEMY * self.difficulty + 
                     CONFIG.DUNGEON.SPAWN_RATE_TREASURE + 
                     CONFIG.DUNGEON.SPAWN_RATE_TRAP):
            self._spawn_trap(room)
        else:
            room.event_type = RoomEventType.EMPTY

    def _spawn_enemy(self, room: Room):
        room.event_type = RoomEventType.ENEMY
        choice = random.random()
        if choice < 0.3:
            enemy = CaveSpider()
        elif choice < 0.6:
            enemy = GoblinGrunt()
        elif choice < 0.85:
            enemy = Skeleton()
        else:
            enemy = Zombie()
        
        enemy.scale_difficulty(self.difficulty)
        room.enemy = enemy

    def _spawn_boss(self, room: Room):
        room.event_type = RoomEventType.ENEMY
        boss = random.choice([WolfBoss(), OgreBoss(), VampireBoss()])
        boss.scale_difficulty(self.difficulty)
        room.enemy = boss

    def _spawn_treasure(self, room: Room):
        room.event_type = RoomEventType.TREASURE
        loot_pool = [SmallHPotion, MediumHPotion, ShortSword, ShortBow, WizardsRobe, LeatherArmor]
        room.treasure.append(random.choice(loot_pool))

    def _spawn_trap(self, room: Room):
        room.event_type = RoomEventType.TRAP
        trap_types = [
            {"name": "spike trap", "damage": 8},
            {"name": "poison needle", "damage": 5, "status": "weakened"},
            {"name": "falling rocks", "damage": 12},
        ]
        room.trap = random.choice(trap_types)

    def _assign_description(self, room: Room):
        descriptions = [
            "a damp stone chamber", "a narrow corridor", "a collapsed hall",
            "a room lit by bioluminescent moss", "a cavern with dripping water",
            "an ancient throne room", "a forgotten library"
        ]
        room.description = "You see " + random.choice(descriptions) + "."

    # --- Display Logic (Refactored) ---
    
    def display_map(self, player_pos: Tuple[int, int], reveal_visited: bool = False):
        print(f"\n╔{'═' * (self.width * 2 - 1)}╗")
        for y in range(self.height):
            row_str = self._build_map_row(y, player_pos, reveal_visited)
            print(f"║{row_str}║")
        print(f"╚{'═' * (self.width * 2 - 1)}╝")

    def _build_map_row(self, y: int, player_pos: Tuple[int, int], reveal_visited: bool) -> str:
        row_symbols = []
        for x in range(self.width):
            room = self.map[y][x]
            symbol = self._get_room_symbol(room, (x, y) == player_pos, reveal_visited)
            row_symbols.append(symbol)
        return " ".join(row_symbols)

    def _get_room_symbol(self, room: Room, is_player: bool, reveal_visited: bool) -> str:
        if is_player:
            return "P"
        if room.is_exit:
            return "E"
        if not reveal_visited or not room.visited:
            return "?"
        
        if room.enemy: return "M"
        if room.treasure: return "T"
        if room.trap: return "!"
        return "."

    # --- Exploration Logic (Refactored) ---

    def explore_from(self, player: Player, battle_callback: Callable) -> bool:
        x, y = self.start_pos
        self._enter_dungeon_msg()
        
        while True:
            room = self.get_room(x, y)
            room.visited = True
            
            self._render_room_state(room, x, y)
            
            if not self._resolve_room_event(room, player, battle_callback):
                return False  # Died
            
            if room.is_exit:
                return self._handle_exit(player)
            
            next_pos = self._prompt_movement(x, y)
            if not next_pos:
                break # Quit
            x, y = next_pos
            
        print("🚪 You retreat from the dungeon.")
        return True

    def _enter_dungeon_msg(self):
        print("\n" + "=" * 50)
        print("🏰 You step into the dungeon...".center(50))
        print("=" * 50)

    def _render_room_state(self, room: Room, x: int, y: int):
        print("\n--- Dungeon Map ---")
        self.display_map((x, y), reveal_visited=True)
        print(f"\n📍 Position: ({x},{y})")
        print(f"   {room.description}")
        print(f"   {room.summary()}")

    def _resolve_room_event(self, room: Room, player: Player, battle_cb: Callable) -> bool:
        """Returns False if player dies, True otherwise."""
        if room.event_type == RoomEventType.TRAP and room.trap:
            return self._handle_trap(room, player)
        
        if room.event_type == RoomEventType.ENEMY and room.enemy:
            return self._handle_combat(room, player, battle_cb)
            
        if room.event_type == RoomEventType.TREASURE and room.treasure:
            self._handle_treasure(room, player)
            
        return True

    def _handle_trap(self, room: Room, player: Player) -> bool:
        trap = room.trap
        print(f"\n⚠️ Trap triggered: {trap['name']}!")
        
        damage = trap.get("damage", 0)
        player.take_damage(damage)
        print(f"💥 {player.name} took {damage} damage!")
        
        if trap.get("status"):
            player.status_effects.append(trap["status"])
            print(f"😵 {player.name} is afflicted with {trap['status']}.")
        
        room.trap = None
        room.event_type = RoomEventType.EMPTY
        return player.is_alive()

    def _handle_combat(self, room: Room, player: Player, battle_cb: Callable) -> bool:
        enemy = room.enemy
        print(f"\n⚔️ An enemy appears: {enemy.name}!")
        battle_cb(player, enemy)
        
        if player.is_alive():
            room.enemy = None
            room.event_type = RoomEventType.EMPTY
            return True
        return False

    def _handle_treasure(self, room: Room, player: Player):
        for item in room.treasure:
            player.inventory.add_item(item)
            print(f"💎 You discovered treasure: {item.name}")
        room.treasure = []
        room.event_type = RoomEventType.EMPTY

    def _handle_exit(self, player: Player) -> bool:
        print("\n" + "=" * 50)
        print("🎉 You found the exit!".center(50))
        reward = int(50 * self.difficulty + 10 * self.depth)
        player.coins += reward
        print(f"💰 You collected {reward} coins.")
        return True

    def _prompt_movement(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        moves = {}
        if self.get_room(x, y - 1): moves['n'] = (x, y - 1)
        if self.get_room(x, y + 1): moves['s'] = (x, y + 1)
        if self.get_room(x - 1, y): moves['w'] = (x - 1, y)
        if self.get_room(x + 1, y): moves['e'] = (x + 1, y)
        
        print("\n🧭 Available moves:", ", ".join([k.upper() for k in moves.keys()]) + " | (Q)uit")
        choice = input("➤ Move (N/S/E/W) or Q: ").strip().lower()
        
        if choice == 'q': return None
        return moves.get(choice)