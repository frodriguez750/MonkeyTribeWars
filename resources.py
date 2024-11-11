import arcade
from enum import Enum
import random
from map_window import pos_to_grid


class ResourceType(Enum):
    WOOD = "WOOD"  # assets from https://kenney.nl/
    STONE = "STONE"
    FOOD = "FOOD"

    def to_sprite_str(self):
        '''Convert resource type to sprite filename.'''
        match self.name:
            case "WOOD":
                return "tree-log-small"  # assets from https://kenney.nl/
            case "STONE":
                return "resource-stone"
            case "FOOD":
                return "burger"
            case _:
                print("Unknown resource type %s.", self.name)
                return


class Resource(arcade.Sprite):
    def __init__(self, type: ResourceType = ResourceType.WOOD, xpos=-1, ypos=-1, randType=False, randPos=False):
        super().__init__()
        if randPos:
            self.center_x, self.center_y = pos_to_grid(random.randint(1, 9), random.randint(1, 9))
        else:
            self.center_x, self.center_y = pos_to_grid(xpos, ypos)

        if randType:
            self.type = random.choice(list(ResourceType))
        else:
            self.type = type

        self.texture = arcade.load_texture(f"assets/images/resources/{self.type.to_sprite_str()}.png")
        self.sprite = arcade.Sprite(self.texture)

    def collected(self):
        """Remove resource from the game and return its type."""
        self.remove_from_sprite_lists()
        return self.type
