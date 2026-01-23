"""
Dungeon generation and exploration system.
Refactored for SOLID:
- SRP: Logic separated from UI and Data Generation.
- DIP: Dependencies (UI, Spawning) are injected via interfaces.
- OCP: Spawning logic is pluggable via Strategy pattern.
"""
import random
from enum import Enum, auto
from typing import List, Tuple, Optional, Callable, Dict, Any, Protocol

from Character.Character_RPG import Player
from items import Item
from config import CONFIG

# ==============================
# ABSTRACTIONS (Interfaces)
# ==============================

class RoomEventType(Enum):
    EMPTY = auto()
    ENEMY = auto()
    TREASURE = auto()
    TRAP = auto()

class DungeonPresenter(Protocol):
    """Abstracts UI and Input for the Dungeon."""
    def show_entrance_msg(self, depth: int) -> None: ...
    def show_exit_msg(self, reward: int) -> None: ...
    def show_room(self, room_desc: str, room_summary: str, map_str: str, x: int, y: int, has_key: bool) -> None: ...
    def show_trap_trigger(self, trap_name: str, damage: int, player_name: str, status: Optional[str]) -> None: ...
    def show_combat_start(self, enemy_name: str) -> None: ...
    def show_treasure_found(self, item_name: str) -> None: ...
    def show_retreat_msg(self) -> None: ...
    def show_key_found(self) -> None: ... # New
    def show_exit_locked(self) -> None: ... # New
    def show_game_complete(self) -> None: ... # New
    def get_movement_input(self, available_moves: List[str]) -> Optional[str]: ...

class SpawnStrategy(Protocol):
    """Abstracts the creation of Enemies, Loot, and Traps."""
    def create_enemy(self, depth: int) -> Any: ...
    def create_boss(self, depth: int) -> Any: ...
    def create_final_boss(self, depth: int) -> Any: ...
    def create_loot(self) -> Item: ...
    def create_trap(self) -> Dict[str, Any]: ...

# ==============================
# DOMAIN ENTITIES
# ==============================

class Room:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.is_exit = False
        self.is_entrance = False
        self.has_key = False # New property
        
        self.event_type: RoomEventType = RoomEventType.EMPTY
        self.enemy: Any = None
        self.treasure: List[Item] = []
        self.trap: Optional[Dict[str, Any]] = None
        
        self.description = "An empty, damp room."
    
    def summary(self) -> str:
        parts = []
        if self.is_entrance: parts.append("Start Point")
        
        if self.enemy: parts.append(f"⚔️ Enemy: {self.enemy.name}")
        elif self.treasure:
            names = ', '.join([t.name for t in self.treasure])
            parts.append(f"💎 Treasure: {names}")
        elif self.trap: parts.append(f"⚠️ Trap: {self.trap['name']}")
        
        if self.has_key: parts.append("🗝️ Rusty Key") # New
            
        if self.is_exit: parts.append("🚪 Exit (Locked)")
            
        if not parts: parts.append("✓ Nothing here.")
        return " | ".join(parts)

class Dungeon:
    def __init__(self, 
                 spawner: SpawnStrategy,
                 presenter: DungeonPresenter,
                 depth: int = 1, 
                 seed: Optional[int] = None):
        
        self.depth = depth
        self._spawner = spawner
        self._presenter = presenter
        
        # Dynamic Map Size (Max 15x15)
        # Increases size every 2 levels roughly
        scale_factor = int(depth * 0.5)
        self.width = min(5 + scale_factor, 15)
        # Make it rectangular sometimes by varying height slightly
        self.height = min(5 + scale_factor + random.randint(0, 2), 15)
        
        if seed is not None:
            random.seed(seed)
        
        self.map: List[List[Room]] = self._generate_grid()
        self.start_pos: Tuple[int, int] = (0, 0)
        self.exit_pos: Tuple[int, int] = (0, 0)
        
        # State tracking for this session
        self.player_has_key = False
        
        self._generate_layout()

    def get_room(self, x: int, y: int) -> Optional[Room]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x]
        return None

    def _generate_grid(self) -> List[List[Room]]:
        return [[Room(x, y) for x in range(self.width)] for y in range(self.height)]

    def _generate_layout(self):
        coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # 1. Place Entrance
        self.start_pos = random.choice(coords)
        coords.remove(self.start_pos)
        start_room = self.get_room(*self.start_pos)
        start_room.is_entrance = True
        start_room.visited = True # Start room is always visited
        start_room.description = "Dungeon entrance: cold stones and the smell of decay."

        # 2. Place Exit (Furthest point logic is better, but random is acceptable per requirements)
        if coords:
            self.exit_pos = random.choice(coords)
            coords.remove(self.exit_pos)
        else:
            self.exit_pos = self.start_pos # Fallback for 1x1 map (unlikely)
            
        exit_room = self.get_room(*self.exit_pos)
        exit_room.is_exit = True
        exit_room.description = "A heavy iron door blocks the way out."

        # 3. Place Key (Must be in a room that is NOT entrance and NOT exit)
        if coords:
            key_pos = random.choice(coords)
            key_room = self.get_room(*key_pos)
            key_room.has_key = True
            key_room.description = "You spot something shiny in the corner."
        else:
            # Fallback: Give key automatically if map is too small
            self.player_has_key = True 

        # 4. Fill content for other rooms
        for y in range(self.height):
            for x in range(self.width):
                room = self.map[y][x]
                if (x, y) == self.start_pos: continue
                
                self._generate_room_content(room)
                # Ensure description is set if not already set by special events
                if not room.is_exit and not room.is_entrance and not room.has_key:
                    self._assign_description(room)

    def _generate_room_content(self, room: Room):
        # Boss Logic: Fixed depths
        if room.is_exit:
            if self.depth == 20:
                self._spawn_boss_final(room)
                return
            elif self.depth in [5, 10, 15]:
                self._spawn_boss(room)
                return
            # Normal exit room has chance for normal boss
            elif random.random() < CONFIG.DUNGEON.SPAWN_RATE_BOSS:
                self._spawn_boss(room)
                return

        # Don't overwrite Key room content logic completely, allow enemies ON TOP of key
        # Standard Roll
        roll = random.random()
        difficulty_modifier = 1.0 + (self.depth * 0.1) # Difficulty scales with depth
        
        if roll < CONFIG.DUNGEON.SPAWN_RATE_ENEMY:
            self._spawn_enemy(room, difficulty_modifier)
        elif roll < (CONFIG.DUNGEON.SPAWN_RATE_ENEMY + CONFIG.DUNGEON.SPAWN_RATE_TREASURE):
            self._spawn_treasure(room)
        elif roll < (CONFIG.DUNGEON.SPAWN_RATE_ENEMY + CONFIG.DUNGEON.SPAWN_RATE_TREASURE + CONFIG.DUNGEON.SPAWN_RATE_TRAP):
            self._spawn_trap(room)
        else:
            room.event_type = RoomEventType.EMPTY

    def _spawn_enemy(self, room: Room, diff: float):
        room.event_type = RoomEventType.ENEMY
        room.enemy = self._spawner.create_enemy(self.depth)
        room.enemy.scale_difficulty(diff)

    def _spawn_boss(self, room: Room):
        room.event_type = RoomEventType.ENEMY
        room.enemy = self._spawner.create_boss(self.depth)
        room.enemy.scale_difficulty(1.0 + (self.depth * 0.1))

    def _spawn_boss_final(self, room: Room):
        room.event_type = RoomEventType.ENEMY
        room.enemy = self._spawner.create_final_boss(self.depth)

    def _spawn_treasure(self, room: Room):
        room.event_type = RoomEventType.TREASURE
        item = self._spawner.create_loot()
        room.treasure.append(item)

    def _spawn_trap(self, room: Room):
        room.event_type = RoomEventType.TRAP
        room.trap = self._spawner.create_trap()

    def _assign_description(self, room: Room):
        descriptions = [
            "a damp stone chamber", "a narrow corridor", "a collapsed hall",
            "a room lit by bioluminescent moss", "a cavern with dripping water",
            "an ancient throne room", "a forgotten library"
        ]
        room.description = "You see " + random.choice(descriptions) + "."

    # --- Display Helper ---
    
    def _generate_map_string(self, player_pos: Tuple[int, int], reveal_visited: bool = False) -> str:
        lines = []
        lines.append(f"╔{'═' * (self.width * 2 - 1)}╗")
        for y in range(self.height):
            row_symbols = []
            for x in range(self.width):
                room = self.map[y][x]
                symbol = self._get_room_symbol(room, (x, y) == player_pos, reveal_visited)
                row_symbols.append(symbol)
            lines.append(f"║{' '.join(row_symbols)}║")
        lines.append(f"╚{'═' * (self.width * 2 - 1)}╝")
        return "\n".join(lines)

    def _get_room_symbol(self, room: Room, is_player: bool, reveal_visited: bool) -> str:
        if is_player: return "P"
        
        # Logic: Exit hidden until visited
        if room.is_exit:
            return "E" if room.visited else "?"
            
        if not reveal_visited or not room.visited: return "?"
        
        if room.enemy: return "M"
        if room.treasure: return "T"
        if room.trap: return "!"
        if room.has_key and not self.player_has_key: return "K"
        return "."

    # --- Exploration Logic ---

    def explore_from(self, player: Player, battle_callback: Callable) -> bool:
        x, y = self.start_pos
        self._presenter.show_entrance_msg(self.depth)
        
        while True:
            room = self.get_room(x, y)
            room.visited = True
            
            # Key Logic
            if room.has_key and not self.player_has_key:
                self.player_has_key = True
                room.has_key = False # Remove key from room
                self._presenter.show_key_found()

            map_str = self._generate_map_string((x, y), reveal_visited=True)
            self._presenter.show_room(room.description, room.summary(), map_str, x, y, self.player_has_key)
            
            if not self._resolve_room_event(room, player, battle_callback):
                return False  # Died
            
            if room.is_exit:
                if self._handle_exit(player):
                    return True # Success
                # If handle_exit returns False, it means locked, continue loop
            
            next_pos = self._prompt_movement(x, y)
            if not next_pos:
                break # Quit
            x, y = next_pos
            
        self._presenter.show_retreat_msg()
        return False # Did not complete dungeon

    def _resolve_room_event(self, room: Room, player: Player, battle_cb: Callable) -> bool:
        if room.event_type == RoomEventType.TRAP and room.trap:
            return self._handle_trap(room, player)
        
        if room.event_type == RoomEventType.ENEMY and room.enemy:
            return self._handle_combat(room, player, battle_cb)
            
        if room.event_type == RoomEventType.TREASURE and room.treasure:
            self._handle_treasure(room, player)
            
        return True

    def _handle_trap(self, room: Room, player: Player) -> bool:
        trap = room.trap
        damage = int(trap.get("damage", 0) * (1 + self.depth * 0.1)) # Scale trap damage
        status = trap.get("status")
        
        player.take_damage(damage)
        if status:
            player.status_effects.append(status)
            
        self._presenter.show_trap_trigger(trap["name"], damage, player.name, status)
        
        room.trap = None
        room.event_type = RoomEventType.EMPTY
        return player.is_alive()

    def _handle_combat(self, room: Room, player: Player, battle_cb: Callable) -> bool:
        enemy = room.enemy
        self._presenter.show_combat_start(enemy.name)
        battle_cb(player, enemy)
        
        if player.is_alive():
            room.enemy = None
            room.event_type = RoomEventType.EMPTY
            return True
        return False

    def _handle_treasure(self, room: Room, player: Player):
        for item in room.treasure:
            player.inventory.add_item(item)
            self._presenter.show_treasure_found(item.name)
        room.treasure = []
        room.event_type = RoomEventType.EMPTY

    def _handle_exit(self, player: Player) -> bool:
        if not self.player_has_key:
            self._presenter.show_exit_locked()
            return False
        
        if self.depth == 20:
            self._presenter.show_game_complete()
        else:
            reward = int(50 * self.depth)
            player.coins += reward
            self._presenter.show_exit_msg(reward)
        return True

    def _prompt_movement(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        moves = {}
        if self.get_room(x, y - 1): moves['n'] = (x, y - 1)
        if self.get_room(x, y + 1): moves['s'] = (x, y + 1)
        if self.get_room(x - 1, y): moves['w'] = (x - 1, y)
        if self.get_room(x + 1, y): moves['e'] = (x + 1, y)
        
        available_keys = [k.upper() for k in moves.keys()]
        choice = self._presenter.get_movement_input(available_keys)
        
        if choice == 'q': return None
        return moves.get(choice)