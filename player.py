import arcade

class Player:
    def __init__(self):
        self.resources = 50
        self.row = 5
        self.col = 5
        self.sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_person/malePerson_idle.png",
            # for above go to https://api.arcade.academy/en/2.6.17/resources.html for sprites
            scale=0.5
        )

    def draw(self):
        """Draw the player sprite."""
        self.sprite.draw()

    def update_position(self, x, y):
        """Update player's pixel position on the grid."""
        self.sprite.center_x = x
        self.sprite.center_y = y

    def handle_key_press(self, key):
        """Move the player or perform actions based on key press."""
        if key == arcade.key.UP:
            self.row = max(0, self.row - 1)
        elif key == arcade.key.DOWN:
            self.row = min(9, self.row + 1)
        elif key == arcade.key.LEFT:
            self.col = max(0, self.col - 1)
        elif key == arcade.key.RIGHT:
            self.col = min(9, self.col + 1)
