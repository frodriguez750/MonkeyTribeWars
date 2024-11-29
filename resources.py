"""
Module: resources
Description: This module handles the management of resources in the game, including their types,
spawning, collection, and interactions with other entities. Resources include wood, stone, and food,
which are critical for gameplay mechanics such as building structures and maintaining player health.
"""

import arcade
import random
from enum import Enum
from game_utils import pos_to_grid, GridSprite
from game_constants import TILE_SIZE

class ResourceType(Enum):
    """
    Enumeration of different resource types available in the game.
    """
    WOOD = "WOOD"
    STONE = "STONE"
    FOOD = "FOOD"

    def to_sprite_str(self):
        """
        Convert a resource type to its corresponding sprite filename.
        Returns:
            str: The filename for the resource sprite.
        """
        match self.name:
            case "WOOD":
                return "tree-log-small"
            case "STONE":
                return "resource-stone"
            case "FOOD":
                return "burger"
            case _:
                print("Unknown resource type %s.", self.name)
                return None

class Resource(arcade.Sprite):
    """
    Represents a resource object in the game, such as wood, stone, or food.
    """
    def __init__(self, type: ResourceType = ResourceType.WOOD, row=None, col=None):
        """
        Initialize a resource object.
        Args:
            type (ResourceType): The type of the resource.
            row (int): Row of the resource in grid units.
            col (int): Column of the resource in grid units.
        """
        super().__init__()

        # Assign random type if not provided
        self.type = type

        # Assign row and column positions
        self.row = random.randint(0, 49) if row is None else row
        self.col = random.randint(0, 49) if col is None else col

        # Set pixel position based on grid coordinates
        self.center_x, self.center_y = pos_to_grid(self.row, self.col, TILE_SIZE)

        # Load the appropriate texture for the resource
        self.texture = arcade.load_texture(
            f"assets/images/resources/{self.type.to_sprite_str()}.png")

    def collected(self):
        """
        Handle the collection of the resource.
        Removes the resource from the game and returns its type.
        Returns:
            ResourceType: The type of the collected resource.
        """
        self.remove_from_sprite_lists()
        return self.type

class ResourceManager:
    """
    Manages the spawning and collection of resources in the game.
    """

    def __init__(self):
        """Initialize the ResourceManager with a sprite list to track resources."""
        self.resource_sprite_list = arcade.SpriteList()

    def spawn_resource(self, is_diamond=False):
        """
        Spawn a single resource or diamond at a random grid location.
        Args:
            is_diamond (bool): If True, spawns a diamond instead of a standard resource.
        """
        if is_diamond:
            # Diamonds are a special case, not tied to ResourceType
            row = random.randint(0, 49)
            col = random.randint(0, 49)
            diamond = GridSprite(":resources:images/items/gemBlue.png", 0.5)
            diamond.row = row
            diamond.col = col
            diamond.center_x, diamond.center_y = pos_to_grid(row, col, TILE_SIZE)
            self.resource_sprite_list.append(diamond)
        else:
            # Normal resource spawning
            resource_type = random.choice(list(ResourceType))
            row = random.randint(0, 49)
            col = random.randint(0, 49)
            resource = Resource(type=resource_type, row=row, col=col)
            self.resource_sprite_list.append(resource)

    def spawn_initial_resources(self, count):
        """
        Spawn a specified number of resources and diamonds on the grid.
        Args:
                count (int): The total number of resources to spawn.
        """
        for _ in range(count):
            self.spawn_resource()  # Spawn normal resources
        for _ in range(count // 2):  # Spawn fewer diamonds
            self.spawn_resource(is_diamond=True)

    def check_resource_collection(self, player):
        """
        Check if the player has collected any resources.
        Args:
            player (arcade.Sprite): The player sprite.
        Returns:
            list: A list of collected resource types.
        """
        collected_resources = []
        resources_collected = arcade.check_for_collision_with_list(
            player, self.resource_sprite_list
        )
        for resource in resources_collected:
            if isinstance(resource, Resource):
                collected_resources.append(resource.collected())
                self.spawn_resource()  # Spawn a new resource for every one collected
        return collected_resources

