"""
File:           settings.py
Description:    Handles saving/setting savings for the project
"""
import os

import constants
import yaml
from kivy.logger import Logger


class SettingsManager:
    """Handles the settings for the application"""

    def __init__(self):
        self.current_settings = None

        self.config_path = os.path.join(constants.PROJECT_PATH, "config.yml")

        # Load in the settings file with error protection
        if not os.path.isdir(constants.PROJECT_PATH):
            os.mkdir(constants.PROJECT_PATH)
        if not os.path.isfile(self.config_path):
            self.load_defaults()
        else:
            with open(self.config_path, "r") as f:
                self.current_settings = yaml.safe_load(f)
            if self.current_settings is None or (
                len(self.current_settings) != len(constants.DEFAULT_SETTINGS)
            ):
                self.load_defaults()

    def load_defaults(self):
        """Resets all settings except for the theme and reference point to their defaults"""

        if self.current_settings is None:
            self.current_settings = constants.DEFAULT_SETTINGS.copy()
        else:
            theme = self.current_settings["theme_style"]
            file = self.current_settings["last_used_reference"]
            self.current_settings = constants.DEFAULT_SETTINGS.copy()
            self.current_settings["theme_style"] = theme
            self.current_settings["last_used_reference"] = file

    def set_setting(self, setting, value):
        """Sets a current setting to a new value

        Args:
            setting: The setting value to change
            value: The new value
        """

        self.current_settings[setting] = value

    def save_settings(self):
        """Saves the current settings to a config file"""

        with open(self.config_path, "w") as f:
            Logger.debug(f"SettingsManager: Settings: {self.current_settings}")
            Logger.debug(f"SettingsManager: Saving settings to {self.config_path}")
            yaml.dump(self.current_settings, f)
            Logger.info("SettingManager: Settings saved successfully!")
