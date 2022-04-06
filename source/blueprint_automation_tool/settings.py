import os

import yaml


class SettingsManager:
    def __init__(self):
        self.default_settings = {
            "base_building_height": -60,
            "building_block_choice": "concrete",
            "scaling_factor": 1.0,
            "theme_style": "Light",
            "last_used_reference": None,
            "last_used_game_version": "1.12",
        }
        self.current_settings = None

        self.folder_name = "Project BAT"
        config_file_name = "config.yml"

        self.documents_path = os.path.expanduser("~/Documents")
        self.project_path = os.path.join(self.documents_path, self.folder_name)
        self.config_path = os.path.join(self.project_path, config_file_name)

        # Load in the settings file with error protection
        if not os.path.isdir(self.project_path):
            os.mkdir(self.project_path)
        if not os.path.isfile(self.config_path):
            self.load_defaults()
        else:
            with open(self.config_path, "r") as f:
                self.current_settings = yaml.safe_load(f)
            if self.current_settings is None or (len(self.current_settings) != len(self.default_settings)):
                self.load_defaults()

    def load_defaults(self):
        theme = self.current_settings["theme_style"]
        file = self.current_settings["last_used_reference"]
        self.current_settings = self.default_settings
        self.current_settings["theme_style"] = theme
        self.current_settings["last_used_reference"] = file

    def set_setting(self, setting, value):
        self.current_settings[setting] = value

    def save_settings(self):
        with open(self.config_path, "w") as f:
            print(self.current_settings)
            print(self.config_path)
            yaml.dump(self.current_settings, f)


if __name__ == "__main__":
    s = SettingsManager()
    print(s.current_settings)
