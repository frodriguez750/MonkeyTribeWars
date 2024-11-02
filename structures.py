import arcade

from mapWindow import LEFT_MARGIN, BOTTOM_MARGIN, TILE_SIZE

STRUCTURE_COSTS = {
    "hut": 10,
    "tower": 20
}

class StructureManager:
    def __init__(self):
        self.structures = {}

    def place_structure(self, structure_type, row, col, resources):
        """Place a structure on the grid if resources are sufficient."""
        cost = STRUCTURE_COSTS.get(structure_type, 0)
        if resources >= cost:
            resources -= cost
            self.structures[(row, col)] = structure_type
            return True
        return False

    def draw_structures(self):
        """Draw structures on the grid based on their type."""
        for (row, col), structure_type in self.structures.items():
            color = arcade.color.BEIGE if structure_type == "hut" else arcade.color.DARK_GRAY
            x = LEFT_MARGIN + col * TILE_SIZE + TILE_SIZE / 2
            y = BOTTOM_MARGIN + row * TILE_SIZE + TILE_SIZE / 2
            arcade.draw_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, color)
