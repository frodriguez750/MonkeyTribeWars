import arcade
from player import Player
from enemy import Enemy
from structures import StructureManager
from upgrades import UpgradeManager
from map_window import MapWindow, LEFT_MARGIN, TILE_SIZE, BOTTOM_MARGIN


class GameWindow(MapWindow):
    def __init__(self):
        super().__init__()
        self.player = Player(start_x=100, start_y=100)
        self.enemy = Enemy(start_x=400, start_y=400)
        self.structure_manager = StructureManager()
        self.upgrade_manager = UpgradeManager(self.player)
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Add player and enemy sprites to the respective lists
        self.player_list.append(self.player.sprite)
        self.enemy_list.append(self.enemy.sprite)

    def setup(self):
        """Set up game elements."""
        self.structure_manager.place_structure("hut", 3, 3, self.player.resources)

    def on_draw(self):
        """Render the screen, grid, structures, and sprites."""

        super().on_draw()
        self.structure_manager.draw_structures()
        self.player_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):
        """Handle player key press for movement and actions."""
        self.player.handle_key_press(key)
        x = LEFT_MARGIN + self.player.col * TILE_SIZE + TILE_SIZE / 2
        y = BOTTOM_MARGIN + self.player.row * TILE_SIZE + TILE_SIZE / 2
        self.player.update_position(x, y)

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
