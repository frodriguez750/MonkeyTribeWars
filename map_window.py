import arcade
from arcade.types import XYWH
import numpy as np
from abc import abstractmethod

# Constants for screen and grid configuration
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Monkey Tribe Wars - Map Exploration"
TILE_SIZE = 100
GRID_HEIGHT = 30
GRID_WIDTH = 40
# Check and adjust TILE_SIZE so that it fits the screen perfectly
if GRID_WIDTH * TILE_SIZE < SCREEN_WIDTH:
    TILE_SIZE = SCREEN_WIDTH // GRID_WIDTH
if GRID_HEIGHT * TILE_SIZE < SCREEN_HEIGHT:
    TILE_SIZE = SCREEN_HEIGHT // GRID_HEIGHT

# might use ms
PLAYER_MOVEMENT_SPEED = 5

# Calculate margin for centering the grid
GRID_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE
GRID_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE
LEFT_MARGIN = (SCREEN_WIDTH - GRID_PIXEL_WIDTH) // 2
BOTTOM_MARGIN = (SCREEN_HEIGHT - GRID_PIXEL_HEIGHT) // 2


class MapWindow(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.camera = arcade.Camera2D()
        self.map_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)


    def on_draw(self):
        """Render the screen and grid."""
        self.clear()
        self.camera.use()
        for row in range(GRID_HEIGHT):
            for column in range(GRID_WIDTH):
                x, y = pos_to_grid(row, column)
                rect = arcade.types.XYWH(x, y, TILE_SIZE, TILE_SIZE)
                tile_type = self.map_grid[row][column]
                color = arcade.color.GREEN if tile_type == 0 else arcade.color.GRAY
                arcade.draw_rect_filled(rect, color)
                arcade.draw_rect_outline(rect, arcade.color.BLACK, border_width=1)


    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        pass


def pos_to_grid(row, col):
    """Convert row and column coordinates to grid coordinates."""
    x = LEFT_MARGIN + col * TILE_SIZE + TILE_SIZE / 2
    y = BOTTOM_MARGIN + row * TILE_SIZE + TILE_SIZE / 2
    return x, y
