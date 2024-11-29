"""
Module: upgrades
Description: This module manages upgrades in the game, allowing players to enhance their abilities,
AI combat strength, structure durability, and resource efficiency. The UpgradeManager class provides
functionality for purchasing and applying upgrades, ensuring progression throughout gameplay.
"""

class UpgradeManager:
    """
    Manages the upgrades for the player, AI players, and structures in the game.
    """
    def __init__(self, player, ai_players, structure_manager):
        """
        Initialize the UpgradeManager with references to the player, AI players, and structures.
        Args:
            player (GridSprite): The player object to apply upgrades to.
            ai_players (arcade.SpriteList): The list of AI player sprites.
            structure_manager (StructureManager): The structure manager handling all structures.
        """
        self.player = player
        self.ai_players = ai_players
        self.structure_manager = structure_manager

        # Define available upgrades with their costs, levels, and effects
        self.upgrades = {
            "player_speed": {"level": 0, "cost": 10, "effect": 0.2},  # Increases player movement speed
            "ai_combat_strength": {"level": 0, "cost": 20, "effect": 1.1},  # Improves AI attack strength
            "structure_health": {"level": 0, "cost": 30, "effect": 50},  # Increases structure health
            "resource_efficiency": {"level": 0, "cost": 15, "effect": 1.2},  # Increases resource collection rate
        }

    def purchase_upgrade(self, upgrade_name, diamonds):
        """
        Purchase an upgrade if the player has enough diamonds.
        Args:
            upgrade_name (str): The name of the upgrade to purchase.
            diamonds (int): The player's current diamond count.
        Returns:
            tuple: (bool, int) - True if the purchase was successful, and the updated diamond count.
        """
        upgrade = self.upgrades.get(upgrade_name)
        if upgrade and diamonds >= upgrade["cost"]:
            diamonds -= upgrade["cost"]
            upgrade["level"] += 1
            upgrade["cost"] = int(upgrade["cost"] * 1.5)  # Increase the cost for the next level
            print(f"{upgrade_name} upgraded to level {upgrade['level']}.")
            return True, diamonds
        print(f"Not enough diamonds for {upgrade_name}.")
        return False, diamonds

    def apply_upgrades(self):
        """
        Apply the effects of all upgrades to the player, AI players, and structures.
        """
        # Upgrade player movement speed
        if self.upgrades["player_speed"]["level"] > 0:
            self.player.speed += self.upgrades["player_speed"]["level"] * self.upgrades["player_speed"]["effect"]

        # Upgrade AI combat strength
        if self.upgrades["ai_combat_strength"]["level"] > 0:
            for ai in self.ai_players:
                ai.attack_strength *= self.upgrades["ai_combat_strength"]["level"] * self.upgrades["ai_combat_strength"]["effect"]

        # Upgrade structure health
        if self.upgrades["structure_health"]["level"] > 0:
            for structure in self.structure_manager.structures:
                structure.health += self.upgrades["structure_health"]["level"] * self.upgrades["structure_health"]["effect"]

        # Upgrade resource efficiency for player
        if self.upgrades["resource_efficiency"]["level"] > 0:
            self.player.resource_gathering_speed *= self.upgrades["resource_efficiency"]["level"] * self.upgrades["resource_efficiency"]["effect"]
