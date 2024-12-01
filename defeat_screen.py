import arcade
from arcade.gui import UIManager, UIButtonRow, UILabel

from music import MusicManager


class DefeatScreen(arcade.View):
    """
    Defeat Screen displayed when the player loses the game.
    """
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        print("UIManager created for defeat screen.")

    def on_show_view(self):
        """
        Called when the defeat screen is shown.
        """
        self.manager.enable()
        print("Defeat screen enabled.")

        # Set the background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        print("Background color set.")

        # Create a vertical layout for UI elements
        button_row = UIButtonRow(vertical=True, align="center", space_between=40)
        print("Button row created.")

        # Add a "YOU WERE DEFEATED!" label using UILabel
        defeat_label = UILabel(
            text="YOU WERE DEFEATED!",
            font_size=60,  # Large font size for emphasis
            text_color=arcade.color.RED,  # Red text color
            bold=True,  # Make the text bold
            align="center",
        )
        self.manager.add(defeat_label)
        defeat_label.center_on_screen()
        defeat_label.move(dy=200)  # Move the label 200 pixels up
        print("Defeat label added as a UILabel and positioned upward.")

        # Add a "Restart" button
        restart_button = button_row.add_button(label="Restart")
        restart_button.style.update(
            {"font_size": "30px"}  # Larger button font size for better visibility
        )
        print("Restart button added to button row.")

        @restart_button.event("on_click")
        def on_restart(event):
            print("Restart button clicked!")
            from main_game import GridGame  # Import the main game view
            music_manager = MusicManager()  # Create a new instance of MusicManager
            music_manager.load_background_music("assets/audio/background_music.wav")  # Load music
            game_view = GridGame(music_manager=music_manager)  # Pass the MusicManager instance
            self.window.show_view(game_view)  # Restart the game

        # Add a "Quit" button
        quit_button = button_row.add_button(label="Quit")
        quit_button.style.update(
            {"font_size": "30px"}  # Larger button font size for better visibility
        )
        print("Quit button added to button row.")

        @quit_button.event("on_click")
        def on_quit(event):
            print("Quit button clicked!")
            arcade.close_window()  # Quit the game

        # Add the button row to the UI Manager
        self.manager.add(button_row)
        print("Button row added to UIManager.")

        # Position the button row below the defeat label
        button_row.center_on_screen()
        button_row.move(dy=-50)  # Move it slightly downward relative to the screen center
        print("Button row positioned below the defeat label.")

    def on_hide_view(self):
        """
        Called when the defeat screen is hidden.
        """
        self.manager.disable()
        print("Defeat screen disabled.")

    def on_draw(self):
        """
        Render the defeat screen.
        """
        self.clear()  # Clear the screen
        print("Rendering defeat screen...")
        self.manager.draw()
