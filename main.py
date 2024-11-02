import arcade
from player import Player
from enemy import Enemy
from structures import StructureManager
from upgrades import UpgradeManager
from map_window import MapWindow

# error here -> TypeError: _type_ must have storage info
class GameWindow(MapWindow):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.enemy = Enemy()
        self.structure_manager = StructureManager()
        self.upgrade_manager = UpgradeManager(self.player)

    def on_draw(self):
        """Render the screen, grid, structures, and sprites."""
        super().on_draw()
        self.structure_manager.draw_structures()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        """Handle player key press for movement and actions."""
        self.player.handle_key_press(key)
        x = LEFT_MARGIN + self.player.col * TILE_SIZE + TILE_SIZE / 2
        y = BOTTOM_MARGIN + self.player.row * TILE_SIZE + TILE_SIZE / 2
        self.player.update_position(x, y)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
