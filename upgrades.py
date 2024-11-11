class UpgradeManager:
    def __init__(self, player=None):
        self.player = player
        self.upgrades = {
            "gathering_speed": {"cost": 20, "effect": 1.5},
            "combat_strength": {"cost": 30, "effect": 1.2},
            'resource_speed': {'level': 0, 'cost': 100},
            'tower_defense': {'level': 0, 'cost': 150},
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

    def purchase_upgrade(self, upgrade_name, resources):
        upgrade = self.upgrades[upgrade_name]
        if resources >= upgrade['cost']:
            resources -= upgrade['cost']
            upgrade['level'] += 1
            upgrade['cost'] *= 1.5
            return True, resources
        return False, resources

    def apply_upgrades(self, monkeys, towers):
        if self.upgrades['resource_speed']['level'] > 0:
            for monkey in monkeys:
                monkey.gathering_speed += self.upgrades['resource_speed']['level'] * 0.1
        if self.upgrades['tower_defense']['level'] > 0:
            for tower in towers:
                tower.health += self.upgrades['tower_defense']['level'] * 10
