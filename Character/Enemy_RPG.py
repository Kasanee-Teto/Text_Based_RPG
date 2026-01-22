"""
Enemy classes for RPG Game.
Defines all enemy types with unique behaviors.
"""
from Character.Character_RPG import Character, Player
from config import ENEMY_STATS, BOSS_STATS

class Enemy(Character):
    """
    Base class for all enemies
    
    Attributes:
        exp_reward (int): EXP given to player on defeat
        defeated_count (int): Times this enemy type has been defeated
    """
    
    def __init__(self, name: str, hp: int, attack: int, defense: int, exp_reward: int):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward
        self.defeated_count = 0
    
        """
        Scale enemy stats by difficulty factor
        
        Args:
            factor: Multiplier for stats (1.0 = normal, 1.5 = 50% harder)
            
        Returns:
            dict: Scaled stats
        """
    def scale_difficulty(self, factor: float = 1.0) -> None:
        self.max_hp = int(self.max_hp * factor)
        self.hp = self.max_hp
        self.attack_power = int(self.attack_power * factor)
        self.defense = int(self.defense * factor)
    
        """
        Handle enemy defeat - award EXP to player
        
        Args:
            player: The victorious player
        """
    def defeated(self, player: Player):
        self.defeated_count += 1
        player.exp += self.exp_reward
        print(f"🏆 {self.name} defeated! {player.name} wins!")
        print(f"💫 {player.name} gained {self.exp_reward} EXP\n")

# Normal Enemies
class GoblinGrunt(Enemy):
    def __init__(self):
        stats = ENEMY_STATS['goblin']
        super().__init__("Goblin Grunt", stats['hp'], stats['attack'], stats['defense'], stats['exp'])

# ==============================
# NORMAL ENEMIES
# ==============================
class CaveSpider(Enemy):
    def __init__(self):
        stats = ENEMY_STATS['spider']
        super().__init__("Cave Spider", stats['hp'], stats['attack'], stats['defense'], stats['exp'])

class Skeleton(Enemy):
    def __init__(self):
        stats = ENEMY_STATS['skeleton']
        super().__init__("Skeleton", stats['hp'], stats['attack'], stats['defense'], stats['exp'])

class Zombie(Enemy):
    def __init__(self):
        stats = ENEMY_STATS['zombie']
        super().__init__("Zombie", stats['hp'], stats['attack'], stats['defense'], stats['exp'])

# Boss Enemies
class WolfBoss(Enemy):
    def __init__(self):
        stats = BOSS_STATS['wolf']
        super().__init__("Alpha Wolf", stats['hp'], stats['attack'], stats['defense'], stats['exp'])
    
    def attack(self, target: Character) -> int:
        dmg = super().attack(target)
        if isinstance(target, Player):
            target.status_effects.append("bleeding")
            print(f"🩸 {target.name} is bleeding!")
        return dmg

class OgreBoss(Enemy):
    def __init__(self):
        stats = BOSS_STATS['ogre']
        super().__init__("Ogre Brute", stats['hp'], stats['attack'], stats['defense'], stats['exp'])
    
    def attack(self, target: Character) -> int:
        dmg = super().attack(target)
        if isinstance(target, Player):
            target.status_effects.append("weakened")
            print(f"💢 {target.name}'s stats are temporarily reduced!")
        return dmg

class VampireBoss(Enemy):
    def __init__(self):
        stats = BOSS_STATS['vampire']
        super().__init__("Vampire Lord", stats['hp'], stats['attack'], stats['defense'], stats['exp'])
    
    def attack(self, target: Character) -> int:
        damage = super().attack(target)
        heal = int(damage * 0.3)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"🧛 {self.name} drains blood! HP recovered {heal} (HP: {self.hp}/{self.max_hp})")
        return damage

class DemonBoss(Enemy):
    def __init__(self):
        stats = BOSS_STATS['demon']
        super().__init__("Demon King", stats['hp'], stats['attack'], stats['defense'], stats['exp'])
    
    def attack(self, target: Character) -> int:
        damage = super().attack(target)
        if isinstance(target, Player):
            target.status_effects.append("bleeding_demon")
            print(f"🩸 {target.name} is severely bleeding!")
            target.status_effects.append("weakened_demon")
            print(f"💢 {target.name}'s stats are severely reduced!")
        
        heal = int(damage * 0.5)
        self.hp = min(self.max_hp, self.hp + heal)
        print(f"😈 {self.name} drains life force and restores {heal} HP!")
        return damage