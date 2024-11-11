import arcade
from map_window import LEFT_MARGIN, TILE_SIZE, BOTTOM_MARGIN

STRUCTURE_COSTS = {
    "hut": {"WOOD": 10},
    "tower": {"WOOD": 10, "STONE": 10}
}


class StructureManager:
    def __init__(self):
        self.structures = {}

    def place_structure(self, structure_type, row, col, resources):
        """Place a structure on the grid if resources are sufficient."""
        cost = STRUCTURE_COSTS.get(structure_type, 0)
        required_str = []
        available_str = []

        for res, amt in cost.items():
            if res in resources:
                # If any resource is insufficient, print error message
                if resources[res] < amt:
                    for req, val in cost.items():
                        required_str.append(req + " " + str(val))
                        available_str.append(req + " " + str(resources.get(req, 0)))

                    print(f"Insufficient resources for {structure_type}. "
                          f"Available: {', '.join(available_str)}. Needed: {', '.join(required_str)}")

                    return False

        for res, amt in cost.items():
            resources[res] -= amt

        self.structures[(row, col)] = structure_type

        return True

    def draw_structures(self):
        """Draw structures on the grid based on their type."""
        for (row, col), structure_type in self.structures.items():
            color = arcade.color.BEIGE if structure_type == "hut" else arcade.color.DARK_GRAY
            x = LEFT_MARGIN + col * TILE_SIZE + TILE_SIZE / 2
            y = BOTTOM_MARGIN + row * TILE_SIZE + TILE_SIZE / 2
            rect = arcade.types.XYWH(x, y, TILE_SIZE, TILE_SIZE)
            arcade.draw_rect_filled(rect, color)
            arcade.draw_rect_outline(rect, arcade.color.BLACK, border_width=1)
