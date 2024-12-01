"""
Module: main_game
Description: The primary game module for "Monkey Tribe Wars," an arcade-style strategy game.
This module handles the initialization of the game window, player and AI setup, resource management,
building placement, enemy interactions, and random game events.
"""

import arcade
import random
from resources import ResourceType, ResourceManager, Resource
from game_utils import GridSprite, pos_to_grid
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT
from buildings import BuildingManager, Hut, Tower
from title_screen import TitleScreen
from upgrades import UpgradeManager
from settings import SettingsMenu
from enemies import Enemy
from music import MusicManager
from defeat_screen import DefeatScreen
# Constants
SCREEN_TITLE = "Monkey Tribe Wars"
RESOURCE_COUNT = 100
SPRITE_SCALING = 0.5
PLAYER_HEALTH = 100
PLAYER_INV = 1  # Duration player is invincible for after taking damage
ENEMY_DAMAGE = 10
ENEMY_MOVE_DELAY = 0.5  # Delay in seconds between enemy moves
BANANA_SPEED = 5
BANANA_LIFE = 1
FLASH_DURATION = 0.25


class GridGame(arcade.View):
    """
        Main class for the "Monkey Tribe Wars" game.
        Handles player and AI behaviors, resource collection, building placement, enemy interactions,
        and game events.
        """
    def __init__(self, music_manager):
        """Initialize the game window and set up game variables and systems."""
        super().__init__()

        self.music_manager = music_manager
        self.music_manager.load_background_music("assets/audio/background_music.wav")
        self.music_manager.play_background_music()

        # Camera setup
        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()
        self.resource_sprite_list = arcade.SpriteList()
        self.diamond_sprite_list = arcade.SpriteList()
        self.banana_sprite_list = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()

        # AI players
        self.ai_players = arcade.SpriteList()

        # Player setup
        self.player = GridSprite(
            "assets/images/characters/monkey.png",  # https://opengameart.org/content/cartoon-animals
            SPRITE_SCALING / 3,
        )
        self.player.row = GRID_HEIGHT // 2
        self.player.col = GRID_WIDTH // 2
        self.player.center_x, self.player.center_y = pos_to_grid(self.player.row, self.player.col, TILE_SIZE)
        self.player_sprite_list.append(self.player)
        self.player.direction = (1, 0)
        self.player.itime = 0
        self.player.hit = False
        self.flash_duration = 0
        self.flash_color = (255, 0, 0, 32)

        # UI elements
        settings_button = arcade.Sprite(":resources:onscreen_controls/shaded_light/gear.png",
                                        center_x=SCREEN_WIDTH-30, center_y=SCREEN_HEIGHT-30)
        self.ui_sprite_list.append(settings_button)

        # Resource manager
        self.resource_manager = ResourceManager()
        self.structure_manager = BuildingManager()
        # Initialize inventory for resources
        self.inventory = {"WOOD": 0, "STONE": 0, "FOOD": 0}
        # self.structure_manager.place_structure(Hut, 200, 200, self.inventory, team="player")
        self.upgrade_manager = UpgradeManager(self.player, self.ai_players, self.structure_manager)

        # Initialize resources and enemies
        self.spawn_resources(RESOURCE_COUNT)
        self.spawn_enemies(10)

        # Game variables
        self.player_health = PLAYER_HEALTH
        self.score = 0
        self.enemies_destroyed = 0
        self.enemy_move_timer = 0
        self.ai_players = arcade.SpriteList()  # List to hold AI-controlled players
        self.ai_player_cost = 20  # Cost to create an AI player
        self.ai_move_timer = 0

        # For random events
        self.active_event = None # Current active event
        self.event_timer = 0 # Duration of event
        self.event_cooldown = 30 # Cooldown time between events in secs
        self.time_since_last_event = 0 # Track time since last event

        self.scroll_to_player()

    def spawn_resources(self, count):
        """Spawn resources randomly on the grid."""
        for _ in range(count):
            rand_type = random.choice(
                [ResourceType.WOOD, ResourceType.STONE, ResourceType.FOOD]
            )
            resource = Resource(type=rand_type)
            self.resource_manager.resource_sprite_list.append(resource)

        # Spawn diamonds (currency resources)
        for _ in range(count // 3):  # Fewer diamonds compared to other resources
            diamond = Resource(type=ResourceType.DIAMOND)
            self.diamond_sprite_list.append(diamond)

    def spawn_enemies(self, count):
        """Spawn enemies randomly on the grid."""
        for _ in range(count):
            row = random.randint(0, GRID_HEIGHT - 1)
            col = random.randint(0, GRID_WIDTH - 1)
            enemy = Enemy("assets/images/characters/monkey.png", SPRITE_SCALING / 3)
            enemy.color = arcade.color.RED
            enemy.row = row
            enemy.col = col
            enemy.center_x, enemy.center_y = pos_to_grid(row, col, TILE_SIZE)
            self.enemy_sprite_list.append(enemy)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera.use()

        # Draw grid
        for row in range(GRID_HEIGHT + 1):
            arcade.draw_line(0, row * TILE_SIZE, GRID_WIDTH * TILE_SIZE, row * TILE_SIZE, arcade.color.LIGHT_GRAY)
        for col in range(GRID_WIDTH + 1):
            arcade.draw_line(col * TILE_SIZE, 0, col * TILE_SIZE, GRID_HEIGHT * TILE_SIZE, arcade.color.LIGHT_GRAY)

        # Draw sprites
        self.resource_sprite_list.draw()
        self.diamond_sprite_list.draw()
        self.player_sprite_list.draw()
        self.enemy_sprite_list.draw()
        self.banana_sprite_list.draw()
        self.ai_players.draw()
        self.resource_manager.resource_sprite_list.draw()
        self.structure_manager.draw_structures()

        # Draw UI
        self.ui_camera.use()
        arcade.draw_text(f"Score: {self.score}  Health: {self.player_health}, Enemies Destroyed: {self.enemies_destroyed}",
                        10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(
            f"WOOD: {self.inventory['WOOD']}  STONE: {self.inventory['STONE']}  FOOD: {self.inventory['FOOD']}",
            10,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            16,
        )

        self.ui_sprite_list.draw()

        if self.flash_duration > 0:
            arcade.draw_lbwh_rectangle_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.flash_color)

    @staticmethod
    def move_sprite(sprite, dx, dy):
        """Move a sprite by a grid offset."""
        sprite.row += dy
        sprite.col += dx
        sprite.row = max(0, min(GRID_HEIGHT - 1, sprite.row))
        sprite.col = max(0, min(GRID_WIDTH - 1, sprite.col))
        sprite.center_x, sprite.center_y = pos_to_grid(sprite.row, sprite.col, TILE_SIZE)

    def scroll_to_player(self):
        """Center the camera on the player and prevent it from going outside the grid."""
        visible_width = TILE_SIZE * 10
        visible_height = TILE_SIZE * 10

        grid_pixel_width = GRID_WIDTH * TILE_SIZE
        grid_pixel_height = GRID_HEIGHT * TILE_SIZE

        half_viewport_width = visible_width / 2
        half_viewport_height = visible_height / 2
        margin = TILE_SIZE

        min_x = half_viewport_width
        max_x = grid_pixel_width - half_viewport_width
        min_y = half_viewport_height - margin
        max_y = grid_pixel_height - half_viewport_height + margin

        camera_x = max(min(self.player.center_x, max_x), min_x)
        camera_y = max(min(self.player.center_y, max_y), min_y)

        self.camera.position = (camera_x, camera_y)

    def on_update(self, delta_time):
        """Update game logic."""
        if self.player_health <= 0:
            print("Game Over!")
            defeat_view = DefeatScreen()
            self.window.show_view(defeat_view)  # Shows defeat screen
            return
        
        if self.flash_duration > 0:
            self.flash_duration -= delta_time

        # Apply active upgrades
        self.upgrade_manager.apply_upgrades()

        # Update banana projectiles
        self.banana_sprite_list.update()
        for banana in self.banana_sprite_list:
            banana.angle += 10
            banana.life += delta_time
            enemies_hit = arcade.check_for_collision_with_list(banana, self.enemy_sprite_list)
            for enemy in enemies_hit:
                enemy.remove_from_sprite_lists()
                banana.remove_from_sprite_lists()
                self.score += 5  # Award points for defeating an enemy
                self.enemies_destroyed += 1
                print(f"Enemy defeated! Score: {self.score}")
                # Respawn enemies
                self.spawn_enemies(1)

            if banana.life > BANANA_LIFE:
                banana.remove_from_sprite_lists()

        # Update enemy movement timer
        self.enemy_move_timer += delta_time
        if self.enemy_move_timer >= ENEMY_MOVE_DELAY:
            self.enemy_move_timer = 0
            for enemy in self.enemy_sprite_list:
                if enemy.alive:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    self.move_sprite(enemy, dx, dy)

                    # Check collision with player
                    if arcade.check_for_collision(enemy, self.player):
                        # Enemy collects resources (but not FOOD or DIAMOND)
                        resources_collected = arcade.check_for_collision_with_list(
                            enemy, self.resource_manager.resource_sprite_list
                        )
                        for resource in resources_collected:
                            collected_type = resource.collected()
                            if collected_type in ["WOOD", "STONE"]:
                                enemy.inventory[collected_type] += 1
                                print(f"Enemy collected {collected_type}.")

                        # Enemy builds structures if enough resources are available
                        if enemy.inventory["WOOD"] >= 10:  # Example: Build Hut if enough wood
                            x, y = enemy.row, enemy.col
                            if self.structure_manager.place_structure(Hut, int(x), int(y), enemy.inventory, team="enemy"):
                                print(f"Enemy built a Hut at ({x}, {y}).")
        
        if self.player.itime > PLAYER_INV:
            self.player.hit = False
            self.player.itime = 0

        if not self.player.hit:
            for enemy in self.enemy_sprite_list:
                if arcade.check_for_collision(enemy, self.player):
                    self.player_take_damage(ENEMY_DAMAGE)
        else:
            self.player.itime += delta_time

        # Player collects diamonds
        diamonds_collected = arcade.check_for_collision_with_list(self.player, self.diamond_sprite_list)
        if diamonds_collected:
            for diamond in diamonds_collected:
                diamond.remove_from_sprite_lists()
                self.score += 1  # Increment the score for diamonds

        # Player collects resources
        collected_resources = self.resource_manager.check_resource_collection(self.player)
        for collected_type in collected_resources:
            if collected_type == ResourceType.FOOD:
                if self.player_health < PLAYER_HEALTH:
                    self.player_heal(10)  # Heal player
                    self.inventory["FOOD"] += 1  # Update FOOD inventory
                else:
                    print("Health is full! Food not collected.")
            elif collected_type == ResourceType.WOOD:
                self.inventory["WOOD"] += 1
            elif collected_type == ResourceType.STONE:
                self.inventory["STONE"] += 1

        # AI Player Movement and Actions
        self.ai_move_timer += delta_time
        if self.ai_move_timer >= ENEMY_MOVE_DELAY:
            self.ai_move_timer = 0
            for ai in self.ai_players:
                # Random movement in the grid
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                self.move_sprite(ai, dx, dy)

                # AI attacks nearby enemies
                for enemy in self.enemy_sprite_list:
                    if abs(ai.row - enemy.row) <= 1 and abs(ai.col - enemy.col) <= 1:
                        enemy.remove_from_sprite_lists()
                        print(f"AI player at ({ai.row}, {ai.col}) attacked and defeated an enemy.")
                        break

                # AI collects resources
                resources_collected = arcade.check_for_collision_with_list(ai,
                                                                           self.resource_manager.resource_sprite_list)
                for resource in resources_collected:
                    if isinstance(resource, Resource):
                        collected_type = resource.collected()
                        if collected_type in {"WOOD", "STONE"}:  # AI collects only wood and stone
                            self.inventory[collected_type] += 1
                            print(f"AI player collected {collected_type}. Inventory: {self.inventory}")
                        elif collected_type == "DIAMOND":
                            print("AI ignored DIAMOND.")
                        elif collected_type == "FOOD":
                            print("AI collected FOOD but cannot use it.")
                        # Spawn a new resource after collection
                        self.resource_manager.spawn_resource()

                # AI building logic
                if self.inventory["WOOD"] >= 10:  # Example threshold for a Hut
                    grid_x, grid_y = ai.row, ai.col
                    pixel_x, pixel_y = pos_to_grid(grid_x, grid_y, TILE_SIZE)
                    if self.structure_manager.place_structure(Hut, pixel_x, pixel_y, self.inventory, team="player"):
                        print(f"AI player built a Hut at ({grid_x}, {grid_y}).")

        # Check if any enemies are no longer alive and respawn them
        defeated_enemies = [enemy for enemy in self.enemy_sprite_list if not enemy.alive]
        for enemy in defeated_enemies:
            self.enemy_sprite_list.remove(enemy)
            self.spawn_enemies(1)

        # Update buildings
        self.structure_manager.update_structures(delta_time, self.player_sprite_list, self.ai_players, self.enemy_sprite_list)

        # Update random event timer
        self.time_since_last_event += delta_time
        if self.active_event:
            self.event_timer += delta_time
            if self.active_event == "Monkey Raid":
                self.apply_monkey_raid_effects()
            elif self.active_event == "Resource Shortage":
                self.apply_resource_shortage_effects()
            elif self.active_event == "Meteor Shower":
                self.apply_meteor_shower_effects()
            elif self.active_event == "Diamond Rain":
                self.apply_diamond_rain_effects()
        else:
            self.trigger_random_event()  # Check if it's time to trigger a new event

    def on_key_press(self, key, modifiers):
        """Handle key press for player movement."""
        if key == arcade.key.UP:
            self.move_sprite(self.player, 0, 1)
            self.player.direction = (0, 1)
        elif key == arcade.key.DOWN:
            self.move_sprite(self.player, 0, -1)
            self.player.direction = (0, -1)
        elif key == arcade.key.LEFT:
            self.move_sprite(self.player, -1, 0)
            self.player.direction = (-1, 0)
        elif key == arcade.key.RIGHT:
            self.move_sprite(self.player, 1, 0)
            self.player.direction = (1, 0)
        elif key == arcade.key.SPACE:
            # self.attack_enemies()
            self.throw_banana()

        self.scroll_to_player()  # Call scroll_to_player here to avoid jittery screen

        # Build structures
        if key == arcade.key.H:  # Press 'H' to build a hut
            pos_x = self.player.center_x
            pos_y = self.player.center_y
            success = self.structure_manager.place_structure(Hut, pos_x, pos_y, self.inventory, team="player")
            grid_x, grid_y = int(pos_x // TILE_SIZE), int(pos_y // TILE_SIZE)
            if success:
                print(f"Hut built at ({grid_x}, {grid_y}).")

        if key == arcade.key.T:  # Press 'T' to build a tower
            pos_x = self.player.center_x
            pos_y = self.player.center_y
            success = self.structure_manager.place_structure(Tower, pos_x, pos_y, self.inventory, team="player")
            grid_x, grid_y = int(pos_x // TILE_SIZE), int(pos_y // TILE_SIZE)
            if success:
                print(f"Tower built at ({grid_x}, {grid_y}).")

        if key == arcade.key.C:  # Press 'C' to create an AI player
            self.create_ai_player()

        # Upgrades
        if key == arcade.key.U:  # Upgrade player speed
            success, self.score = self.upgrade_manager.purchase_upgrade("player_speed", self.score)
            if success:
                print("Player speed upgraded!")
            else:
                print("Not enough diamonds for player speed upgrade.")

        if key == arcade.key.I:  # Upgrade AI combat strength
            success, self.score = self.upgrade_manager.purchase_upgrade("ai_combat_strength", self.score)
            if success:
                print("AI combat strength upgraded!")
            else:
                print("Not enough diamonds for AI combat strength upgrade.")

        if key == arcade.key.O:  # Upgrade structure health
            success, self.score = self.upgrade_manager.purchase_upgrade("structure_health", self.score)
            if success:
                print("Structure health upgraded!")
            else:
                print("Not enough diamonds for structure health upgrade.")

        if key == arcade.key.P:  # Upgrade resource efficiency
            success, self.score = self.upgrade_manager.purchase_upgrade("resource_efficiency", self.score)
            if success:
                print("Resource efficiency upgraded!")
            else:
                print("Not enough diamonds for resource efficiency upgrade.")

    def on_mouse_press(self, x, y, button, modifiers):
        for ui in self.ui_sprite_list:
            if ui.collides_with_point((x, y)):
                settings_view = SettingsMenu(self, self.music_manager)  # Pass this view as the parent
                self.window.show_view(settings_view)

    def attack_enemies(self):
        """Attack enemies adjacent to the player and destroy them."""
        for enemy in self.enemy_sprite_list:
            if abs(self.player.row - enemy.row) <= 1 and abs(self.player.col - enemy.col) <= 1:
                enemy.remove_from_sprite_lists()
                self.score += 5  # Award points for defeating an enemy
                self.enemies_destroyed += 1
                print(f"Enemy defeated! Score: {self.score}")
                # Respawn enemies
                self.spawn_enemies(1)
    
    def throw_banana(self):
        """Throw a banana in front of the player."""
        banana = arcade.Sprite()
        banana.texture = arcade.load_texture("assets/images/projectiles/banana.png")
        banana.center_x, banana.center_y = self.player.center_x, self.player.center_y
        banana.direction = self.player.direction
        banana.change_x, banana.change_y = banana.direction[0] * BANANA_SPEED, banana.direction[1] * BANANA_SPEED
        banana.life = 0
        self.banana_sprite_list.append(banana)

    def player_take_damage(self, damage):
        self.player_health -= damage
        self.flash_duration = FLASH_DURATION
        self.player.hit = True
        self.flash_color = (255, 0, 0, 32)
    
    def player_heal(self, health):
        self.player_health = max(self.player_health + health, PLAYER_HEALTH)
        self.flash_duration = FLASH_DURATION
        self.flash_color = (0, 255, 0, 32)

    def create_ai_player(self):
        """Create a new AI player if the player has enough points."""
        if self.score >= self.ai_player_cost:
            self.score -= self.ai_player_cost  # Deduct points for the new AI player
            new_ai = GridSprite(
                ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png",  # Replace with AI player sprite image path
                SPRITE_SCALING
            )
            # Assign AI-specific attributes, such as movement behavior
            new_ai.row = int(new_ai.center_y // TILE_SIZE)
            new_ai.col = int(new_ai.center_x // TILE_SIZE)
            self.ai_players.append(new_ai)
            print(f"AI player created! Remaining score: {self.score}")
        else:
            print(f"Not enough points to create AI player! Current score: {self.score}")

    def apply_meteor_shower_effects(self):
        """
        Apply effects of the "Meteor Shower" event.
        """
        meteor_duration = 5  # Event lasts for 5 seconds
        if self.event_timer >= meteor_duration:
            print("Meteor Shower ended!")
            self.active_event = None
        else:
            # Damage all structures and nearby entities
            for structure in self.structure_manager.structures:
                structure.health -= 20
                if structure.health <= 0:
                    self.structure_manager.structures.remove(structure)
                    print(f"A structure was destroyed by the meteor shower!")

            # Damage players and enemies in random spots
            for sprite_list in [self.player_sprite_list, self.enemy_sprite_list]:
                for sprite in sprite_list:
                    if random.random() < 0.1:  # 10% chance to be hit
                        if type(sprite) is GridSprite:
                            self.player_take_damage(10)
                            print("Player was hit by a meteor!")
                        else:
                            sprite.health -= 10
                            print(f"{sprite.__class__.__name__} was hit by a meteor!")
                            if sprite.health <= 0:
                                sprite.remove_from_sprite_lists()
                                print(f"{sprite.__class__.__name__} was destroyed by a meteor!")

    def apply_monkey_raid_effects(self):
        """
        Apply effects of the "Monkey Raid" event.
        """
        raid_duration = 10  # Event lasts for 10 seconds
        if self.event_timer >= raid_duration:
            # Reset effects after the raid ends
            for enemy in self.enemy_sprite_list:
                enemy.speed = max(enemy.speed - 1, 1)  # Ensure speed doesn't go below 1
                enemy.attack_power = max(enemy.attack_power - 5, 1)
            print("Monkey Raid ended!")
            self.active_event = None
        else:
            # Increase enemy speed and attack power during the raid
            for enemy in self.enemy_sprite_list:
                enemy.speed += 1
                enemy.attack_power += 5
            print("Monkey Raid in progress!")

    def apply_resource_shortage_effects(self):
        """
        Apply effects of the "Resource Shortage" event.
        """
        shortage_duration = 15  # Event lasts for 15 seconds
        if self.event_timer >= shortage_duration:
            print("Resource shortage ended!")
            self.active_event = None
        else:
            # Temporarily reduce resource availability
            for resource in self.resource_manager.resource_sprite_list:
                resource.type = random.choice([ResourceType.WOOD, ResourceType.STONE])  # Reduce variety
            print("Resource shortage in progress!")

    def apply_diamond_rain_effects(self):
        """
        Apply effects of the "Diamond Rain" event.
        """
        rain_duration = 10  # Event lasts for 10 seconds
        if self.event_timer >= rain_duration:
            print("Diamond Rain ended!")
            self.active_event = None
        else:
            # Spawn extra diamonds randomly on the map
            for _ in range(5):  # Spawn 5 diamonds per tick
                diamond = Resource(ResourceType.DIAMOND)
                self.diamond_sprite_list.append(diamond)
                print(f"Diamond spawned at ({diamond.row}, {diamond.col})")

    def trigger_random_event(self):
        """
        Trigger a random event to add unpredictability to the game.
        """
        if self.active_event is None and self.time_since_last_event >= self.event_cooldown:
            # Add new events to the list
            events = ["Monkey Raid", "Resource Shortage", "Meteor Shower", "Diamond Rain"]
            self.active_event = random.choice(events)
            self.event_timer = 0  # Reset event timer
            self.time_since_last_event = 0  # Reset cooldown
            print(f"Random event triggered: {self.active_event}")


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    title_screen = TitleScreen(MusicManager())
    window.show_view(title_screen)  # Start with the title screen
    arcade.run()
