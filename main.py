import arcade
from game_window import GameWindow


def main():
    window = arcade.Window(1920, 1080, "Monkey Tribe Wars")
    game_view = GameWindow()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
