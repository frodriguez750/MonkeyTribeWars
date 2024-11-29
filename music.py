"""
Module: music
Description: Handles background music and sound effects for the game.
"""

import arcade

class MusicManager:
    """
    Manages background music and sound effects for the game.
    """

    def __init__(self):
        """
        Initialize the MusicManager with empty tracks and default settings.
        """
        self.background_music = None  # Holds the background music track
        self.sound_effects = {}  # Dictionary to hold sound effects by name
        self.player = None  # Arcade media player
        self.volume = 0.5  # Default volume (50%)

    def load_background_music(self, file_path):
        """
        Load a background music track.

        Args:
            file_path (str): The file path to the background music file.
        """
        self.background_music = arcade.Sound(file_path)

    def load_sound_effect(self, name, file_path):
        """
        Load a sound effect and store it in the dictionary.

        Args:
            name (str): The name of the sound effect (used for lookup).
            file_path (str): The file path to the sound effect file.
        """
        self.sound_effects[name] = arcade.Sound(file_path)

    def play_background_music(self, loop=True):
        """
        Play the background music.

        Args:
            loop (bool): Whether the music should loop.
        """
        if self.background_music:
            self.player = self.background_music.play(self.volume)

    def stop_background_music(self):
        """
        Stop the background music.
        """
        if self.player:
            self.player.pause()

    def play_sound_effect(self, name):
        """
        Play a sound effect by its name.

        Args:
            name (str): The name of the sound effect to play.
        """
        if name in self.sound_effects:
            self.sound_effects[name].play(self.volume)

    def set_volume(self, volume):
        """
        Set the volume for both music and sound effects.

        Args:
            volume (float): The volume level (0.0 to 1.0).
        """
        self.volume = volume
        if self.player:
            self.player.volume = volume
