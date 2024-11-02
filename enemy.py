import numpy as np

class Enemy:
    def __init__(self):
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
