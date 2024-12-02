"""
Module: buildings
Description: Contains classes for game structures such as huts and towers, along with functionality
for managing construction, resource costs, and interactions like spawning entities or attacking.
"""

import arcade
from enemies import Enemy
from game_constants import TILE_SIZE

# Costs required to build different types of structures
STRUCTURE_COSTS = {
    "hut": {"WOOD": 10},  # A hut costs 10 units of wood
    "tower": {"WOOD": 10, "STONE": 10}  # A tower costs 10 units of wood and stone each
}

# Constants
BUILDING_ATTACK_DAMAGE = 20  # Damage dealt by buildings
BUILDING_ATTACK_RANGE = 2  # Range of attack (twice that of players/enemies)
PLAYER_SPAWN_COOLDOWN = 10  # Time in seconds between player spawns
ENEMY_SPAWN_COOLDOWN = 10  # Time between enemy spawns in seconds


class Structure(arcade.Sprite):
    """
    A generic class for structures in the game, such as huts or towers.

    Attributes:
        cost (dict): Resources required to build the structure.
        health (int): Health of the structure.
        team (str): The team the structure belongs to ('player' or 'enemy').
        spawn_timer (float): Timer to track entity spawning.
        attack_timer (float): Timer to track attack intervals.
    """
    def __init__(self, image_path, start_x, start_y, cost, health, scale, team):
        """
        Initialize a generic structure.
        Args:
            image_path (str): Path to the sprite image for the structure.
            start_x (int): X-coordinate in pixels.
            start_y (int): Y-coordinate in pixels.
            cost (dict): Resources required to build the structure.
            health (int): Health of the structure.
            scale (float): Scaling factor for the sprite.
            team (str): The team the structure belongs to ('player' or 'enemy').
        """
        # Initialize the parent class with the sprite's image and position
        super().__init__(image_path, center_x=start_x, center_y=start_y, scale=scale)
        self.cost = cost  # Cost to build the structure
        self.health = health  # Health of the structure
        self.texture = arcade.load_texture(image_path)  # Load the texture for the structure
        self.sprite = arcade.Sprite(self.texture)  # Create the sprite with the texture
        self.spawn_timer = 0
        self.attack_timer = 0
        self.team = team # Either player or enemy

    def take_damage(self, amount):
        """
        Reduce the health of the structure by the specified amount.

        Args:
            amount (int): Amount of damage to apply.
        """
        self.health -= amount
        if self.health <= 0:
            self.remove_from_sprite_lists()
            print(f"{self.__class__.__name__} destroyed!")

    def spawn_entity(self, entity_list, tile_size):
        """
        Spawn an entity (AI player or enemy) at the structure's location.

        Args:
            entity_list (arcade.SpriteList): List to which the spawned entity will be added.
            tile_size (int): The size of a grid tile in pixels.
        """
        if self.team == "player" and self.spawn_timer >= PLAYER_SPAWN_COOLDOWN:
            # Spawn a player-aligned AI at the building's location
            new_ai = arcade.Sprite(
                "assets/images/characters/monkey.png",
                scale=0.15,
            )
            new_ai.center_x = self.center_x
            new_ai.center_y = self.center_y
            new_ai.row, new_ai.col = int(self.center_y // tile_size), int(self.center_x // tile_size)
            entity_list.append(new_ai)
            self.spawn_timer = 0
            print(f"AI Player spawned at ({self.center_x}, {self.center_y}) by {self.__class__.__name__}")
        elif self.team == "enemy" and self.spawn_timer >= ENEMY_SPAWN_COOLDOWN:
            # Spawn an enemy at the building's location
            new_enemy = Enemy("assets/images/characters/monkey.png", scaling=0.5)
            new_enemy.color = arcade.color.RED
            new_enemy.center_x = self.center_x
            new_enemy.center_y = self.center_y
            new_enemy.row, new_enemy.col = int(self.center_y // tile_size), int(self.center_x // tile_size)
            entity_list.append(new_enemy)
            self.spawn_timer = 0
            print(f"Enemy spawned at ({self.center_x}, {self.center_y}) by {self.__class__.__name__}")

    def attack_nearby_entities(self, target_list, range_tiles, damage):
        """
        Attack all entities within a specified range.

        Args:
            target_list (arcade.SpriteList): List of targets to attack.
            range_tiles (int): Range of the attack in grid tiles.
            damage (int): Amount of damage dealt to each target.
        """
        for target in target_list:
            distance = ((self.center_x - target.center_x) ** 2 + (self.center_y - target.center_y) ** 2) ** 0.5
            if distance <= range_tiles * TILE_SIZE:
                if hasattr(target, 'health'): # Check if target has health attribute
                    target.health -= damage
                    print(
                        f"{self.__class__.__name__} attacked {target.__class__.__name__} at ({target.row}, {target.col})!")
                    if target.health <= 0:
                        target.alive = False
                        target.remove_from_sprite_lists()
                        print(f"{target.__class__.__name__} was destroyed!")


class Hut(Structure):
    """
    A specific type of structure representing a hut.

    Attributes:
        team (str): The team the hut belongs to ('player' or 'enemy').
    """
    def __init__(self, start_x, start_y, team):
        """
        Initialize a hut structure.
        Args:
            start_x (int): X-coordinate in pixels.
            start_y (int): Y-coordinate in pixels.
            team (str): The team the hut belongs to ('player' or 'enemy').
        """
        # Call the parent class with specific values for a hut
        super().__init__('assets/images/resources/hut.png', start_x, start_y, cost={"WOOD": 5}, health=100, scale=0.15, team=team)
        self.team = team

class Tower(Structure):
    """
    A specific type of structure representing a tower.

    Attributes:
        team (str): The team the tower belongs to ('player' or 'enemy').
    """
    def __init__(self, start_x, start_y, team):
        """
        Initialize a tower structure.
        Args:
            start_x (int): X-coordinate in pixels.
            start_y (int): Y-coordinate in pixels.
            team (str): The team the tower belongs to ('player' or 'enemy').
        """
        # Call the parent class with specific values for a tower
        super().__init__('assets/images/resources/tower.png', start_x, start_y, cost={"WOOD": 75, "STONE": 25}, health=200, scale=0.15, team=team)
        self.team = team

class BuildingManager:
    """
    A class to manage and track all structures in the game.
    """
    def __init__(self):
        """
        Manage and track all structures in the game.
        """
        # List to hold all structure sprites
        self.structures = arcade.SpriteList()

    def place_structure(self, structure_type, x, y, resources, team):
        """
        Place a structure on the grid if resources are sufficient.
        Args:
            structure_type (class): The type of structure to place (e.g., Hut, Tower).
            x (int): X-coordinate in pixels.
            y (int): Y-coordinate in pixels.
            resources (dict): The player's available resources.
            team (str): The team that the structure belongs to ("player" or "enemy").
        Returns:
            bool: True if the structure was placed successfully, False otherwise.
        """
        # Create an instance of the specified structure type
        structure = structure_type(x, y, team)
        cost = structure.cost  # Get the cost to build the structure
        required_str = []  # List for required resource strings
        available_str = []  # List for available resource strings
        insufficient = False

        # Check if the player has enough resources to build the structure
        for res, amt in cost.items():
            if resources.get(res, 0) < amt:
                insufficient = True
                required_str.append(f"{res} {amt}")
                available_str.append(f"{res} {resources.get(res, 0)}")

        # If a resource is insufficient, log an error message and exit
        if insufficient:
            print(f"Insufficient resources for {structure_type.__name__}. "
                  f"Available: {', '.join(available_str)}. Needed: {', '.join(required_str)}")
            return False

        # Deduct the required resources from the player's inventory
        for res, amt in cost.items():
            resources[res] -= amt

        # Add the structure to the list and log success
        self.structures.append(structure)
        print(f"{structure_type.__name__} successfully placed.")
        return True

    def draw_structures(self):
        """
        Draw all structures on the screen.
        """
        self.structures.draw()  # Use the sprite list's draw method to render structures

    def update_structures(self, delta_time, player_list, ai_list, enemy_list):
        """
        Update all structures for spawning and attacking.

        Args:
            delta_time (float): Time elapsed since the last update.
            player_list (arcade.SpriteList): List of player-controlled sprites.
            ai_list (arcade.SpriteList): List of AI-controlled sprites.
            enemy_list (arcade.SpriteList): List of enemy sprites.
        """
        for structure in self.structures:
            structure.spawn_timer += delta_time
            structure.attack_timer += delta_time

            # Spawn entities based on team
            if structure.team == "player":
                structure.spawn_entity(ai_list, TILE_SIZE)
                if structure.attack_timer >= 1:
                    structure.attack_nearby_entities(enemy_list, BUILDING_ATTACK_RANGE, BUILDING_ATTACK_DAMAGE)
            elif structure.team == "enemy":
                structure.spawn_entity(enemy_list, TILE_SIZE)
                if structure.attack_timer >= 1:
                    structure.attack_nearby_entities(player_list, BUILDING_ATTACK_RANGE, BUILDING_ATTACK_DAMAGE)
                    structure.attack_nearby_entities(ai_list, BUILDING_ATTACK_RANGE, BUILDING_ATTACK_DAMAGE)
                structure.attack_timer = 0
