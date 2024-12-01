"""
Module: settings.py

Description:
This module defines the `SettingsMenu` class, which provides a settings interface
for controlling game options such as volume and returning to the main game.
"""

import arcade
from arcade.gui import UIManager, UIBoxLayout, UISlider, UIFlatButton, UITextWidget, UILabel
from arcade.gui.events import UIOnClickEvent
from game_constants import SCREEN_HEIGHT, SCREEN_WIDTH


class SettingsMenu(arcade.View):
    """
    A view for the game's settings menu, allowing players to adjust options
    such as volume and return to the main game.
    """

    def __init__(self, game_view, music_manager):
        """
        Initialize the settings menu.

        Args:
            game_view (arcade.View): A reference to the main game view.
        """
        super().__init__()
        self.game_view = game_view  # Reference to the main game view
        self.manager = UIManager()
        self.music_manager = music_manager  # Reference to the music manager
        self.volume = 0.5  # Initial volume level (0-100)
        print("SettingsMenu initialized.")

    def on_show_view(self):
        """
        Called when the settings menu is shown.
        Sets up the UI elements and enables the UIManager.
        """
        self.manager.enable()
        print("SettingsMenu enabled.")

        # Set the background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        print("Background color set.")

        # Create box layout for settings
        settings_layout = UIBoxLayout(vertical=True, align="center", space_between=20,
                                         x=SCREEN_WIDTH / 2 - 150, y=SCREEN_HEIGHT / 2)

        self.volume_label = UITextWidget(text="Volume", align="center")
        settings_layout.add(self.volume_label)

        # Add volume slider
        self.volume_slider = UISlider(min_value=0, max_value=1, value=self.volume, width=300, align="center")
        settings_layout.add(self.volume_slider)

        # Add "how to play" button
        how_to_play_button = UIFlatButton(text="How to Play")
        settings_layout.add(how_to_play_button)

        @how_to_play_button.event("on_click")
        def on_how_to_play(event: UIOnClickEvent):
            self.display_how_to_play()

        # Add a back button to return to the game
        back_button = UIFlatButton(text="Back")
        settings_layout.add(back_button)

        @back_button.event("on_click")
        def on_back(event: UIOnClickEvent):
            self.return_to_game()

        self.manager.add(settings_layout)


    def on_hide_view(self):
        """
        Called when the settings menu is hidden.
        Disables the UIManager.
        """
        self.manager.disable()
        print("SettingsMenu disabled.")

    def on_draw(self):
        """
        Render the settings menu.
        Clears the screen and draws the UI elements.
        """
        self.clear()
        self.manager.draw()
        # print("SettingsMenu rendered.")

    def on_update(self, delta_time):
        """
        Update settings values.
        """
        self.volume = self.volume_slider.value
        self.music_manager.set_volume(self.volume)

    def display_how_to_play(self):
        """
        Display the "How to Play" instructions as an overlay.
        """
        # Clear previous UI components
        self.manager.clear()

        # Create a vertical layout for the instructions
        how_to_play_layout = UIBoxLayout(vertical=True, align="center", space_between=10,
                                         x=SCREEN_WIDTH / 2 - 150, y=SCREEN_HEIGHT / 2 - 150)

        # Add instructions
        instructions = [
            "How to Play:",
            "Spacebar: Attack",
            "H: Build a Hut",
            "T: Build a Tower",
            "C: Create AI Player",
            "U: Upgrade Player Speed",
            "I: Upgrade Combat Strength",
            "O: Upgrade Structure Health",
            "P: Upgrade Resource Efficiency",
            "Press Back to Return"
        ]

        for line in instructions:
            label = UILabel(text=line, font_size=16, text_color=arcade.color.WHITE)
            how_to_play_layout.add(label)

        # Add a back button to return to settings
        back_button = UIFlatButton(text="Back")
        how_to_play_layout.add(back_button)

        @back_button.event("on_click")
        def on_back(event: UIOnClickEvent):
            self.manager.clear()  # Clear the "How to Play" UI
            self.on_show_view()  # Reload the main settings menu

        self.manager.add(how_to_play_layout)

    def return_to_game(self):
        """
        Return to the main game view.
        Disables the UIManager and switches back to the game view.
        """
        self.manager.disable()
        self.window.show_view(self.game_view)
        print("Returning to the main game.")
