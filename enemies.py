"""
Module: enemies
Description: Defines enemy behaviors, attributes, and interactions with other game entities.
Provides classes for managing enemy-specific logic such as resource collection and inventory management.
"""


from game_utils import GridSprite

class Enemy(GridSprite):
    """
    Custom Enemy class inheriting from GridSprite to include attributes for resource collection
    and building behavior.

    Attributes:
        alive (bool): Indicates whether the enemy is alive.
        inventory (dict): Tracks the resources the enemy has collected (e.g., "WOOD", "STONE").
        attack_power (int): The attack power of the enemy for damaging structures or players.
    """
    def __init__(self, image, scaling, health=100):
        """
        Initializes an Enemy object with default attributes.

        Args:
            image (str): The path to the enemy's sprite image.
            scaling (float): The scaling factor for the enemy's sprite.
            health (int): Initial health of the enemy.
        """
        super().__init__(image, scaling)
        self.alive = True
        self.inventory = {"WOOD": 0, "STONE": 0}  # Enemy inventory for building resources
        self.attack_power = 5  # Default attack power
        self.health = health
