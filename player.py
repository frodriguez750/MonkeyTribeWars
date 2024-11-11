import arcade


class Player:
    def __init__(self, start_x, start_y, scale=0.5):
        # Initialize player sprite and position
        self.sprite = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", scale)
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y
        self.resources = {
            "WOOD":  50,
            "STONE": 50,
            "FOOD":  50
        }
        self.row = 5
        self.col = 5

    def update_position(self, x, y):
        """Update player's pixel position on the grid."""
        self.sprite.center_x = x
        self.sprite.center_y = y

    def handle_key_press(self, key):
        """Move the player or perform actions based on key press."""
        if key == arcade.key.UP:
            self.row = max(0, self.row + 1)
        elif key == arcade.key.DOWN:
            self.row = min(9, self.row - 1)
        elif key == arcade.key.LEFT:
            self.col = max(0, self.col - 1)
        elif key == arcade.key.RIGHT:
            self.col = min(9, self.col + 1)
