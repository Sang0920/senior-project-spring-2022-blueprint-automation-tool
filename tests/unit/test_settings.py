from blueprint_automation_tool.constants import DEFAULT_SETTINGS
from blueprint_automation_tool.settings import SettingsManager

manager = SettingsManager()


def test_load_defaults():
    manager.load_defaults()
    assert (
        manager.current_settings["base_building_height"] == DEFAULT_SETTINGS["base_building_height"]
    )
    assert (
        manager.current_settings["building_block_choice"]
        == DEFAULT_SETTINGS["building_block_choice"]
    )
    assert manager.current_settings["scaling_factor"] == DEFAULT_SETTINGS["scaling_factor"]
    assert manager.current_settings["theme_style"] == DEFAULT_SETTINGS["theme_style"]
    assert (
        manager.current_settings["last_used_game_version"]
        == DEFAULT_SETTINGS["last_used_game_version"]
    )


def test_save_settings():
    assert manager.save_settings() is None


def test_set_setting():
    manager.set_setting("base_building_height", 10)
    assert manager.current_settings["base_building_height"] == 10

    manager.set_setting("building_block_choice", "wool")
    assert manager.current_settings["building_block_choice"] == "wool"

    manager.set_setting("scaling_factor", 1.2)
    assert manager.current_settings["scaling_factor"] == 1.2

    manager.set_setting("theme_style", "Light")
    assert manager.current_settings["theme_style"] == "Light"

    manager.set_setting("last_used_game_version", "1.16")
    assert manager.current_settings["last_used_game_version"] == "1.16"
