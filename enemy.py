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
        self.resource_gathering_rate = 5 # Amt of resources gathered per cycle

    def gather_resources(self):
        """Enemy gathers resources periodically."""
        self.resources += self.resource_gathering_rate
        print(f"Enemy gathered resources. Total resources: {self.resources}")

    def place_structure(self):
        """Enemy places structures on the grid if it has enough resources."""
        if self.resources >= 10:  # Example structure cost
            row, col = np.random.randint(0, 10), np.random.randint(0, 10)
            if self.structures[row, col] is None:
                self.structures[row, col] = "hut"
                self.resources -= 10
                print(f"Placed structure at ({row}, {col}")



    def engage_in_combat(self, opponent):
        """Determine whether to attack or defend based on resources and opponent strength."""
        if self.resources >= 20: # Threshold to attack
            print("Enemy is attacking!")
            self.resources -= 20 # cost of attacking
            # Logic for attacking opponent (ex: reduce their health)
            opponent.take_damage(10) # assume opponent has take_damage method
        else:
            print("Enemy is defending due to low resources!")
            # Logic for defense (ex: increase defense or avoid attack)
            self.resources += 2 # Regain small amt of resources while defending

    def make_decision(self, grid):
        """Decide the next action based on the current grid state."""
        # Simple logic to move towards resources or engage in combat
        resource_positions = np.argwhere(grid == 1)  # Assuming 1 represents a resource tile
        if len(resource_positions) > 0:
            target_position = resource_positions[0]  # Move towards the first resource found
            print(f"Enemy moving towards resource at {target_position}")
            # Update the sprite position (simplified movement logic)
            self.sprite.center_x += (target_position[1] - self.sprite.center_x) * 0.1
            self.sprite.center_y += (target_position[0] - self.sprite.center_y) * 0.1
        else:
            print("No resources found. Enemy is staying put.")