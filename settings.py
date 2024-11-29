"""
Module: settings.py

Description:
This module defines the `SettingsMenu` class, which provides a settings interface
for controlling game options such as volume and returning to the main game.
"""

import arcade
from arcade.gui import UIManager, UIButtonRow
from arcade.gui.events import UIOnClickEvent


class SettingsMenu(arcade.View):
    """
    A view for the game's settings menu, allowing players to adjust options
    such as volume and return to the main game.
    """

    def __init__(self, game_view):
        """
        Initialize the settings menu.

        Args:
            game_view (arcade.View): A reference to the main game view.
        """
        super().__init__()
        self.game_view = game_view  # Reference to the main game view
        self.manager = UIManager()
        self.volume = 50  # Initial volume level (0-100)
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

        # Create a button row to organize buttons vertically
        button_row = UIButtonRow(vertical=True, align="center", space_between=20)

        # Add volume control buttons
        volume_up_button = button_row.add_button(label="Volume Up")
        print("Volume Up button added.")

        @volume_up_button.event("on_click")
        def on_volume_up(event: UIOnClickEvent):
            self.volume_up()

        volume_down_button = button_row.add_button(label="Volume Down")
        print("Volume Down button added.")

        @volume_down_button.event("on_click")
        def on_volume_down(event: UIOnClickEvent):
            self.volume_down()

        # Add a back button to return to the game
        back_button = button_row.add_button(label="Back to Game")
        print("Back to Game button added.")

        @back_button.event("on_click")
        def on_back(event: UIOnClickEvent):
            self.return_to_game()

        # Add the button row to the UI Manager
        self.manager.add(button_row)
        print("Button row added to UIManager.")

        # Center the button row on the screen
        button_row.center_on_screen()
        print("Button row centered on the screen.")

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
        print("SettingsMenu rendered.")

    def volume_up(self):
        """
        Increase the game volume by 10%, up to a maximum of 100%.
        """
        if self.volume < 100:
            self.volume += 10
            print(f"Volume increased to {self.volume}%.")
        else:
            print("Volume is already at maximum!")

    def volume_down(self):
        """
        Decrease the game volume by 10%, down to a minimum of 0%.
        """
        if self.volume > 0:
            self.volume -= 10
            print(f"Volume decreased to {self.volume}%.")
        else:
            print("Volume is already at minimum!")

    def return_to_game(self):
        """
        Return to the main game view.
        Disables the UIManager and switches back to the game view.
        """
        self.manager.disable()
        self.window.show_view(self.game_view)
        print("Returning to the main game.")