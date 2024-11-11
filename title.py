import arcade
import arcade.gui
from arcade.types import XYWH

class TitleScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the play button
        play_button = arcade.gui.UIFlatButton(text="PLAY", width=200)
        play_button.on_click = self.on_click_play
        self.v_box.add(play_button)

        # Create a widget to hold the v_box widget, centering the buttons
        self.manager.add(
            arcade.gui.UIAnchorLayout(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """Render the title screen."""
        self.clear()
        # Draw the background rectangle using XYWH
        background_rect = XYWH(0, 0, self.window.width, self.window.height)
        arcade.draw_rectangle_filled(
            background_rect.center_x,
            background_rect.center_y,
            background_rect.width,
            background_rect.height,
            arcade.color.DARK_BLUE_GRAY
        )

        # Draw the title using arcade.Text
        title_text = arcade.Text(
            "Monkey Tribe Wars",
            self.window.width // 2,
            self.window.height - 150,
            color=arcade.color.WHITE,
            font_size=80,
            anchor_x="center"
        )
        title_text.draw()



        # Draw the UI manager elements (buttons)
        self.manager.draw()


    def on_click_play(self, _event=None):
        """Handle click event for the play button."""
        print("Play button clicked")
        from game_window import GameWindow
        game_view = GameWindow()
        self.window.show_view(game_view)

