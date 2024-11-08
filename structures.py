import arcade
from map_window import LEFT_MARGIN, TILE_SIZE, BOTTOM_MARGIN

STRUCTURE_COSTS = {
    "hut": 10,
    "tower": 20
}

class Structure(arcade.Sprite):
    def __init__(self, image_path, start_x, start_y, cost, health):
        super().__init__(image_path, center_x=start_x, center_y=start_y)
        self.cost = cost
        self.health = health
class Hut(Structure):
    def __init__(self, start_x, start_y):
        super().__init__('images/hut.png', start_x, start_y, cost=50, health=100)

class Tower(Structure):
    def __init__(self, start_x, start_y):
        super().__init__('images/tower.png', start_x, start_y, cost=100, health=200)

class StructureManager:
    def __init__(self):
        self.structures = []

    def place_structure(self, structure_type, x, y, resources):
        if resources >= structure_type.cost:
            new_structure = structure_type(x,y)
            self.structures.append(new_structure)
            resources -= structure_type.cost
            return True, resources
        return False, resources

    def draw_structures(self):
        for structure in self.structures:
            structure.draw()