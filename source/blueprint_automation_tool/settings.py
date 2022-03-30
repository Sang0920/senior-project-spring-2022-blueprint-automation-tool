import os

import yaml


class SettingsManager:
    def __init__(self):
        self.default_settings = {
            "base_building_height": -60,
            "building_block_choice": "concrete",
            "scaling_factor": 1.0,
        }

        self.current_settings = None

        self.folder_name = "Project BAT"
        self.config_file_name = "config.yml"

        self.expanded_documents_path = os.path.expanduser("~/Documents/")
        self.project_folder_path = os.path.join(self.expanded_documents_path, self.folder_name)
        self.config_file_path = os.path.join(self.project_folder_path, self.config_file_name)

        self.load_settings()

    def load_settings(self):
        # Make the project directory for the config file if it doesn't exist
        if not os.path.isdir(self.project_folder_path):
            os.mkdir(self.project_folder_path)

        if not os.path.isfile(self.config_file_path):
            self.current_settings = self.default_settings
            self.save_settings()
        else:
            with open(self.config_file_path, "r") as f:
                self.current_settings = yaml.safe_load(f)

    def get_settings(self):
        if not self.current_settings:
            self.load_settings()
        return self.current_settings

    def update_setting(self, setting, value):
        if not self.current_settings:
            self.load_settings()
        self.current_settings[setting] = value

    def save_settings(self):
        with open(self.config_file_path, "w") as f:
            yaml.dump(self.current_settings, f)


if __name__ == "__main__":
    s = SettingsManager()
    print(s.get_settings())
