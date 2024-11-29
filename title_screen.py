"""
Module: title_screen
Description: Implements the title screen of the game with options to start the game, open settings, or exit.
"""

import arcade
from arcade.gui import UIManager, UIButtonRow
from arcade.gui.events import UIOnClickEvent
from settings import SettingsMenu  # Import your settings menu module


class TitleScreen(arcade.View):
    """
    Represents the title screen of the game.
    """

    def __init__(self):
        super().__init__()
        # Initialize the UI Manager
        self.manager = UIManager()

    def on_show_view(self):
        """
        Called when the view is shown.
        """
        self.manager.enable()

        # Set the background color
        self.window.background_color = arcade.color.DARK_BLUE_GRAY

        # Create the title text
        self.title_text = arcade.Text(
            "Monkey Tribe Wars",
            self.window.width // 2,
            self.window.height - 150,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )

        # Create a button row
        button_row = UIButtonRow(vertical=True, align="center", space_between=20)

        # Add the "PLAY" button
        play_button = button_row.add_button(label="PLAY")
        @play_button.event("on_click")
        def on_play_click(event: UIOnClickEvent):
            from main_game import GridGame  # Import your game class
            game_view = GridGame()
            self.window.show_view(game_view)

        # Add the "SETTINGS" button
        settings_button = button_row.add_button(label="Settings")
        @settings_button.event("on_click")
        def on_settings_click(event: UIOnClickEvent):
            settings_view = SettingsMenu(self)  # Pass this view as the parent
            self.window.show_view(settings_view)

        # Add the "EXIT" button
        exit_button = button_row.add_button(label="EXIT")
        @exit_button.event("on_click")
        def on_exit_click(event: UIOnClickEvent):
            arcade.exit()

        # Add the button row to the UI Manager
        self.manager.add(button_row)

        # Center the button row on the screen
        button_row.center_on_screen()

    def on_hide_view(self):
        """
        Called when the view is hidden.
        """
        self.manager.disable()

    def on_draw(self):
        """
        Render the title screen.
        """
        self.clear()  # Clear the screen
        self.title_text.draw()  # Draw the title text
        self.manager.draw()  # Draw the UI components
