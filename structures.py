import arcade
from map_window import LEFT_MARGIN, TILE_SIZE, BOTTOM_MARGIN

STRUCTURE_COSTS = {
    "hut": {"WOOD": 10},
    "tower": {"WOOD": 10, "STONE": 10}
}


class Structure(arcade.Sprite):
    def __init__(self, image_path, start_x, start_y, cost, health, scale):
        super().__init__(image_path, center_x=start_x, center_y=start_y, scale=scale)
        self.cost = cost
        self.health = health
        self.texture = arcade.load_texture(image_path)
        self.sprite = arcade.Sprite(self.texture)


class Hut(Structure):
    def __init__(self, start_x, start_y):
        super().__init__('assets/images/resources/hut.png', start_x, start_y, cost={"WOOD": 50}, health=100, scale=0.25)


class Tower(Structure):
    def __init__(self, start_x, start_y):
        super().__init__('assets/images/resources/tower.png', start_x, start_y, cost={"WOOD": 75, "STONE": 25}, health=200, scale=0.25)


class StructureManager:
    def __init__(self):
        self.structures = arcade.SpriteList()

    def place_structure(self, structure_type, x, y, resources):
        """Place a structure on the grid if resources are sufficient."""
        structure = structure_type(x, y)
        cost = structure.cost
        required_str = []
        available_str = []

        for res, amt in cost.items():
            if res in resources:
                # If any resource is insufficient, print error message
                if resources[res] < amt:
                    for req, val in cost.items():
                        required_str.append(req + " " + str(val))
                        available_str.append(req + " " + str(resources.get(req, 0)))

                    print(f"Insufficient resources for {structure_type.__name__}. "
                          f"Available: {', '.join(available_str)}. Needed: {', '.join(required_str)}")

                    return False

        for res, amt in cost.items():
            resources[res] -= amt

        self.structures.append(structure)
        print(f"{structure_type.__name__} successfully placed.")
        return True

    def draw_structures(self):
        self.structures.draw()
