import arcade
import random

from arcade.examples.astar_pathfinding import VIEWPORT_MARGIN
from arcade.examples.background_blending import CAMERA_SPEED

from player import Player
from enemy import Enemy
from structures import StructureManager, Hut
from upgrades import UpgradeManager
from map_window import MapWindow, pos_to_grid, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, LEFT_MARGIN, \
    TILE_SIZE, BOTTOM_MARGIN
from resources import Resource

VIEWPORT_MARGIN = 10
CAMERA_SPEED = 1

class GameWindow(MapWindow):
    def __init__(self):
        super().__init__()
        # Calculate the center of the map in terms of grid positions
        center_col = GRID_WIDTH // 2
        center_row = GRID_HEIGHT // 2
        # Convert grid positions to pixel coordinates
        start_x = LEFT_MARGIN + (GRID_WIDTH // 2) * TILE_SIZE + TILE_SIZE // 2
        start_y = BOTTOM_MARGIN + (GRID_HEIGHT // 2) * TILE_SIZE + TILE_SIZE // 2
        # Set the player to be in the middle of the map
        self.player = Player(start_x, start_y)
        self.enemies = [
            Enemy(random.randint(100, GRID_WIDTH * TILE_SIZE - 100), random.randint(100, GRID_HEIGHT * TILE_SIZE - 100))
            for _ in range(4)]

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.resource_list = arcade.SpriteList()

        # Add player and enemy sprites to the respective lists
        self.player_list.append(self.player.sprite)
        for enemy in self.enemies:
            self.enemy_list.append(enemy.sprite)

        self.structure_manager = StructureManager()
        self.upgrade_manager = UpgradeManager(self.player)

        self.generate_resources(10)

        self.view_left = 0
        self.view_bottom = 0
        #self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera = arcade.Camera2D(window=self.window)

    def on_update(self, delta_time):
        """Update game logic, including enemy AI actions"""
        self.player_list.update()
        self.enemy_list.update()
        for enemy in self.enemies:
            if hasattr(enemy, 'make_decision'):
                enemy.make_decision(self.map_grid)
            if enemy.sprite.collides_with_sprite(self.player.sprite):
                enemy.engage_in_combat(self.player)

        self.scroll_to_player()


    def scroll_to_player(self):
        """Scroll the camera to keep the player within the viewport margins."""
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player.sprite.left

        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.sprite.right > right_boundary:
            self.view_left += self.player.sprite.right - right_boundary

        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.sprite.top > top_boundary:
            self.view_bottom += self.player.sprite.top - top_boundary

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.sprite.bottom

        # Update camera position smoothly
        self.camera.position = (self.view_left, self.view_bottom, CAMERA_SPEED)

    def setup(self):
        """Set up game elements."""
        self.structure_manager.place_structure("hut", 3, 3, self.player.resources)

    def on_draw(self):
        """Render the screen, grid, structures, and sprites."""
        self.clear()
        self.camera.use()
        super().on_draw()

        self.structure_manager.draw_structures()
        self.player_list.draw()
        self.enemy_list.draw()
        self.resource_list.draw()


    def on_key_press(self, key, modifiers):
        """Handle player key press for movement and actions."""
        if key == arcade.key.UP and self.player.row < GRID_HEIGHT - 1:
            self.player.row += 1
        elif key == arcade.key.DOWN and self.player.row > 0:
            self.player.row -= 1
        elif key == arcade.key.LEFT and self.player.col > 0:
            self.player.col -= 1
        elif key == arcade.key.RIGHT and self.player.col < GRID_WIDTH - 1:
            self.player.col += 1

        if key == arcade.key.P:  # Example key for placing a hut
            placed, self.player.resources = self.structure_manager.place_structure(Hut, self.player.sprite.center_x,
                                                                                   self.player.sprite.center_y,                                                                  self.player.resources)
            if placed:
                print("Hut placed!")
            else:
                print("Not enough resources!")


        # Update the player's position on the screen
        x, y = pos_to_grid(self.player.row, self.player.col)
        self.player.update_position(x, y)

        # Center the camera on the player
        self.scroll_to_player()

    def check_resource(self):
        """Check if the player is on a resource cell and collects the resource."""
        for resource in self.resource_list:
            if arcade.check_for_collision(self.player.sprite, resource):
                self.player.resources += 1
                resource.collected()
                self.resource_list.remove(resource)
                break

    def generate_resources(self, quantity):
        """Generate random resources on the map."""
        for _ in range(quantity):
            self.resource_list.append(Resource(randType=True, randPos=True))