import arcade
from player import Player
from enemy import Enemy
from structures import StructureManager
from upgrades import UpgradeManager
from map_window import MapWindow, pos_to_grid
from resources import Resource


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
        self.resource_list = arcade.SpriteList()

        # Add player and enemy sprites to the respective lists
        self.player_list.append(self.player.sprite)
        self.enemy_list.append(self.enemy.sprite)
        self.generate_resources(5)

    def setup(self):
        """Set up game elements."""
        self.structure_manager.place_structure("hut", 3, 3, self.player.resources)

    def on_draw(self):
        """Render the screen, grid, structures, and sprites."""

        super().on_draw()
        self.structure_manager.draw_structures()
        self.player_list.draw()
        self.enemy_list.draw()
        self.resource_list.draw()

    def on_key_press(self, key, modifiers):
        """Handle player key press for movement and actions."""
        self.player.handle_key_press(key)
        x, y = pos_to_grid(self.player.row, self.player.col)
        self.player.update_position(x, y)
        self.check_resource()

    def check_resource(self):
        """Check if the player is on a resource cell and collects the resource."""
        for resource in self.resource_list:
            if arcade.check_for_collision(self.player.sprite, resource):
                self.player.resources[resource.collected().name] += 5
                break

    def generate_resources(self, quantity):
        """Generate random resources on the map."""
        for _ in range(quantity):
            self.resource_list.append(Resource(randType=True, randPos=True))


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
