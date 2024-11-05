import arcade
import numpy as np

class Enemy:
    def __init__(self, start_x, start_y, scale=0.5):
        # Initialize enemy sprite and position
        self.sprite = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", scale)
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        # Enemy resources and structures
        self.resources = 50
        self.structures = np.full((10, 10), None)

    def gather_resources(self):
        """Enemy gathers resources periodically."""
        self.resources += 5

    def place_structure(self):
        """Enemy places structures on the grid if it has enough resources."""
        if self.resources >= 10:  # Example structure cost
            row, col = np.random.randint(0, 10), np.random.randint(0, 10)
            if self.structures[row, col] is None:
                self.structures[row, col] = "hut"
                self.resources -= 10

    #def draw(self):
     #   """Draw the enemy sprite."""
      #  self.sprite.draw()
