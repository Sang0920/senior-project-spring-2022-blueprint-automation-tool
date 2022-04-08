import os
import sys
import tkinter
from math import degrees
from tkinter import filedialog

from builder import PlaceBuilder
from color_matcher import color_to_minecraft_dye
from game_automation import AutomationException, GameAutomator
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from place_parser import PlaceParser
from settings import SettingsManager
from window import WindowHandler

Config.set("input", "mouse", "mouse,multitouch_on_demand")

Settings = SettingsManager()

root = tkinter.Tk()
root.withdraw()


class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Settings reference by UI and automation
        self.app_name = "Blueprint Automation Tool"
        self.loaded_reference = None
        self.loaded_build_places = None
        self.window_manager = WindowHandler()

        # Main Screen for the application
        self.screen = Builder.load_file("main.kv")

        # Menu Options
        blocks = [
            {
                "text": "Concrete",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="concrete": self.on_block_menu_update(x),
            },
            {
                "text": "Concrete Powder",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="concrete_powder": self.on_block_menu_update(x),
            },
            {
                "text": "Wool",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="wool": self.on_block_menu_update(x),
            },
            {
                "text": "Terracotta",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="terracotta": self.on_block_menu_update(x),
            },
            {
                "text": "Glazed Terracotta",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="glazed_terracotta": self.on_block_menu_update(x),
            },
            {
                "text": "Stained Glass",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="stained_glass": self.on_block_menu_update(x),
            },
        ]

        # Dynamically Created Widgets
        self.dialog = None
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.block_drop_down,
            items=blocks,
            width_mult=4,
        )

    def build(self):
        self.title = self.app_name
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = Settings.current_settings["theme_style"]
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Brown"

        return self.screen

    def on_start(self):
        self.update_settings_values()
        if Settings.current_settings["last_used_reference"]:
            if os.path.isfile(Settings.current_settings["last_used_reference"]):
                self.load_reference(Settings.current_settings["last_used_reference"])

    # APPLICATION CALLBACKS

    def on_block_menu_update(self, block_type, *args):
        formatted_block = block_type.replace("_", " ").title()
        Settings.current_settings["building_block_choice"] = block_type
        self.root.ids.block_drop_down.text = formatted_block
        print(formatted_block)

    def on_build_places(self, *args):
        print("Building!")
        try:
            builder = PlaceBuilder()
            builder.build_place(
                self.loaded_reference,
                self.loaded_build_places,
                Settings.current_settings["base_building_height"],
                Settings.current_settings["building_block_choice"],
                Settings.current_settings["scaling_factor"],
            )

            parser = PlaceParser()
            for file in self.loaded_build_places:
                found_place = parser.parse_place(file)[0]
                color = color_to_minecraft_dye(found_place.color).replace("_", " ").title()
                num_points = len(found_place.coordinate_list)
                item = ThreeLineListItem(
                    text=found_place.name,
                    secondary_text=f"Color: {color}",
                    tertiary_text=f"Corners: {num_points}",
                )
                self.root.ids.build_history_list.add_widget(item)
        except AutomationException as e:
            print(f"ERROR: {e.message}")
            self.open_alert_dialog(f"Automation has been halted. {e.message}")

        self.window_manager.set_current_window(self.window_manager.find_window(self.app_name)[0])

    def on_detect_minecraft_version(self, show_error=True, *args):
        try:
            automator = GameAutomator()
            version = automator.find_minecraft_version()
            self.root.ids.minecraft_version_label.text = version
            Settings.set_setting("last_used_game_version", version)
        except AutomationException:
            print("Minecraft Not Found")
            self.root.ids.minecraft_version_label.text = "1.18"
            Settings.set_setting("last_used_game_version", "1.18")
            if show_error:
                print("Showing alert dialog")
                self.open_alert_dialog("Minecraft not found. Defaulting to Minecraft version 1.18")

    def on_load_places(self, *args):
        # Prompt user to load files
        paths = filedialog.askopenfilenames(
            title="Pick Places To Build", filetypes=(("KML", "*.kml"), ("KMZ", "*.kmz"))
        )
        print(paths)
        if paths:
            parser = PlaceParser()
            self.root.ids.loaded_places_list.clear_widgets()
            self.loaded_build_places = paths
            for file in paths:
                found_place = parser.parse_place(file)[0]
                color = color_to_minecraft_dye(found_place.color).replace("_", " ").title()
                num_points = len(found_place.coordinate_list)
                item = ThreeLineListItem(
                    text=found_place.name,
                    secondary_text=f"Color: {color}",
                    tertiary_text=f"Corners: {num_points}",
                )
                self.root.ids.loaded_places_list.add_widget(item)
        print(paths)

    def on_load_reference(self, *args):
        # Prompt User to select a reference file
        path = filedialog.askopenfilename(
            title="Pick A Reference Point", filetypes=(("KML", "*.kml"), ("KMZ", "*.kmz"))
        )
        if path and os.path.isfile(path):
            self.load_reference(path)
        print(path)

    def on_reset_settings(self, *args):
        self.open_confirmation_dialog("Reset Settings?", "Are you sure?", self.reset_settings)

    def on_darkmode_toggle(self, switch, value, *args):
        if value:
            self.theme_cls.theme_style = "Dark"
            Settings.set_setting("theme_style", "Dark")
        else:
            self.theme_cls.theme_style = "Light"
            Settings.set_setting("theme_style", "Light")

    def on_slider_change(self, slider, textfield, setting, *args):
        value = int(args[1])
        textfield.text = f"{value}"
        if setting == "scaling_factor":
            value = value / 100.0
        Settings.set_setting(setting, value)

    def on_textfield_change(self, slider, textfield, setting, *args):
        if args[1] and args[1] != "-":
            value = int(args[1])
            if value >= slider.min and value <= slider.max:
                slider.value = value
                if setting == "scaling_factor":
                    value = value / 100.0
                Settings.set_setting(setting, value)

    # DIALOG FUNCTIONS

    def open_alert_dialog(self, text):
        self.dialog = MDDialog(
            title="Alert!",
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=self.dismiss),
            ],
        )
        self.dialog.open()

    def open_confirmation_dialog(self, title, text, callback):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="Confirm", on_release=callback),
                MDFlatButton(text="Cancel", on_release=self.dismiss),
            ],
        )
        self.dialog.open()

    def dismiss(self, *args):
        self.dialog.dismiss()

    # APPLICATION FUNCTIONALITY

    def load_reference(self, reference_file_path):
        parser = PlaceParser()
        if not reference_file_path:
            self.open_alert_dialog(
                "You must select one file for the automation to use as a reference point."
            )
        else:
            Settings.set_setting("last_used_reference", reference_file_path)
            self.loaded_reference = parser.parse_place(reference_file_path)[0]
            ref_coords = self.loaded_reference.coordinate_list[0]

            name_string = f"[b]Name:[/b] {self.loaded_reference.name}\n\n"
            latitude_string = f"[b]Latitude:[/b] {round(degrees(ref_coords.latitude), 6)}°\n"
            longitude_string = f"[b]Longitude:[/b] {round(degrees(ref_coords.longitude), 6)}°"
            info_string = name_string + latitude_string + longitude_string

            self.root.ids.reference_info_label.text = info_string

    def reset_settings(self, *args):
        self.dismiss()
        print("Resetting to Defaults!")
        Settings.load_defaults()
        print(Settings.current_settings)
        self.update_settings_values()

    def update_settings_values(self, *args):
        print("Updating Labels")
        self.root.ids.block_drop_down.text = (
            Settings.current_settings["building_block_choice"].replace("_", " ").title()
        )
        self.root.ids.scale_value_textfield.text = str(
            int(Settings.current_settings["scaling_factor"] * 100)
        )
        self.root.ids.scale_value_slider.value = Settings.current_settings["scaling_factor"] * 100
        self.root.ids.height_value_textfield.text = str(
            int(Settings.current_settings["base_building_height"])
        )
        self.root.ids.height_value_slider.value = Settings.current_settings["base_building_height"]
        if Settings.current_settings["theme_style"] == "Dark":
            self.root.ids.darkmode_switch.active = True
        else:
            self.root.ids.darkmode_switch.active = False
        self.theme_cls.theme_style = Settings.current_settings["theme_style"]


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
    Settings.save_settings()
