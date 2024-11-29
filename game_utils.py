"""
Module: game_utils
Description: Utility functions and classes for grid-based operations in the game.
"""

import arcade
from game_constants import TILE_SIZE

def pos_to_grid(row, col, tile_size=TILE_SIZE):
    """
    Convert row and column indices to pixel coordinates.

    Args:
        row (int): Row index in the grid.
        col (int): Column index in the grid.
        tile_size (int): Size of each tile in pixels (default is TILE_SIZE).

    Returns:
        tuple: (x, y) pixel coordinates for the center of the tile.
    """
    x = col * tile_size + tile_size / 2
    y = row * tile_size + tile_size / 2
    return x, y

def pos_to_grid_index(center_x, center_y, tile_size):
    """
    Convert pixel coordinates to row and column indices.

    Args:
        center_x (float): X-coordinate in pixels.
        center_y (float): Y-coordinate in pixels.
        tile_size (int): Size of each tile in pixels.

    Returns:
        tuple: (row, col) indices in the grid.
    """
    row = int(center_y // tile_size)
    col = int(center_x // tile_size)
    return row, col


class GridSprite(arcade.Sprite):
    """
    A custom sprite class with additional attributes for grid-based positioning.

    Attributes:
        row (int): The row index in the grid where the sprite is located.
        col (int): The column index in the grid where the sprite is located.
        speed (float): The speed of the sprite for movement calculations.
        resource_gathering_speed (float): The speed of resource collection for the sprite.
    """
    def __init__(self, image, scaling):
        """
        Initialize a GridSprite object.

        Args:
            image (str): Path to the sprite's image file.
            scaling (float): Scaling factor for the sprite.
        """
        super().__init__(image, scaling)
        self.row = 0
        self.col = 0
        self.speed = 1.0
        self.resource_gathering_speed = 1.0

