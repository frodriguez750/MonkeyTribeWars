import arcade
import numpy as np
from abc import ABC, abstractmethod

# Constants for screen and grid configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Monkey Tribe Wars - Map Exploration"
GRID_WIDTH = 10
GRID_HEIGHT = 10
TILE_SIZE = 50

# Calculate margin for centering the grid
GRID_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE
GRID_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE
LEFT_MARGIN = (SCREEN_WIDTH - GRID_PIXEL_WIDTH) // 2
BOTTOM_MARGIN = (SCREEN_HEIGHT - GRID_PIXEL_HEIGHT) // 2


class MapWindow(arcade.Window, ABC):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Initialize grid and player position
        self.map_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.player_row = GRID_HEIGHT // 2
        self.player_col = GRID_WIDTH // 2

    @abstractmethod
    def on_draw(self):
        """Render the screen and grid. Subclasses should extend this."""
        arcade.start_render()
        # Draw the grid
        for row in range(GRID_HEIGHT):
            for column in range(GRID_WIDTH):
                x = LEFT_MARGIN + column * TILE_SIZE + TILE_SIZE / 2
                y = BOTTOM_MARGIN + row * TILE_SIZE + TILE_SIZE / 2
                tile_type = self.map_grid[row][column]

                # Set tile color based on tile type
                color = arcade.color.GREEN if tile_type == 0 else arcade.color.GRAY
                arcade.draw_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, color)
                arcade.draw_rectangle_outline(x, y, TILE_SIZE, TILE_SIZE, arcade.color.BLACK)

    @abstractmethod
    def on_key_press(self, key, modifiers):
        """Handle key presses. Subclasses should define specific actions."""
        pass
