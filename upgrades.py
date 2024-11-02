class UpgradeManager:
    def __init__(self, player):
        self.player = player
        self.upgrades = {
            "gathering_speed": {"cost": 20, "effect": 1.5},
            "combat_strength": {"cost": 30, "effect": 1.2}
        }

    def apply_upgrade(self, upgrade_type):
        """Apply a specific upgrade to the player."""
        upgrade = self.upgrades.get(upgrade_type)
        if upgrade and self.player.resources >= upgrade["cost"]:
            self.player.resources -= upgrade["cost"]
            if upgrade_type == "gathering_speed":
                self.player.gathering_speed *= upgrade["effect"]
            elif upgrade_type == "combat_strength":
                self.player.combat_strength *= upgrade["effect"]
