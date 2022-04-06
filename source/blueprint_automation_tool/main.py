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
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from place_parser import PlaceParser
from settings import SettingsManager
from window import WindowHandler

Config.set("input", "mouse", "mouse,multitouch_on_demand")

Settings = SettingsManager()

root = tkinter.Tk()
root.withdraw()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app_name = "Blueprint Automation Tool"
        self.dialog = None

        self.loaded_reference = None
        self.loaded_build_places = None
        self.builder = PlaceBuilder()
        self.window_manager = WindowHandler()

        self.screen = Builder.load_file("main.kv")
        block_menu_items = [
            {
                "text": "Concrete",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="concrete": self.callback_block_menu(x),
            },
            {
                "text": "Concrete Powder",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="concrete_powder": self.callback_block_menu(x),
            },
            {
                "text": "Wool",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="wool": self.callback_block_menu(x),
            },
            {
                "text": "Terracotta",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="terracotta": self.callback_block_menu(x),
            },
            {
                "text": "Glazed Terracotta",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="glazed_terracotta": self.callback_block_menu(x),
            },
            {
                "text": "Stained Glass",
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x="stained_glass": self.callback_block_menu(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.block_drop_down,
            items=block_menu_items,
            width_mult=4,
        )
        self.dialog = None

    def build(self):
        self.title = self.app_name
        self.theme_cls.theme_style = Settings.current_settings["theme_style"]
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Brown"
        return self.screen

    def on_start(self):
        # Built in function for kivy, runs after loading
        self.update_labels()
        if Settings.current_settings["last_used_reference"]:
            self.load_reference(Settings.current_settings["last_used_reference"])

    def show_alert_dialog(self, text):
        self.dialog = MDDialog(title="Alert:", text=text, buttons=[MDRaisedButton(text="Confirm", on_release=self.close_dialog)])
        self.dialog.open()

    def show_confirmation_dialog(self, title, notification_text, callback):
        self.dialog = MDDialog(
            title=title,
            text=notification_text,
            buttons=[
                MDRaisedButton(text="Confirm", on_release=callback),
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def update_labels(self):
        self.root.ids.block_slider.value = Settings.current_settings["base_building_height"]
        self.root.ids.scale_slider.value = Settings.current_settings["scaling_factor"] * 100
        self.root.ids.block_drop_down.text = Settings.current_settings["building_block_choice"].replace("_", " ").title()
        self.callback_update_game_version(show_error=False)

    def reset_settings(self, obj):
        print("Resetting to Defaults!")
        Settings.load_defaults()
        self.close_dialog(obj)
        self.theme_cls.theme_style = Settings.current_settings["theme_style"]
        self.update_labels()

    def callback_reset_settings(self):
        title = "Reset Settings?"
        text = "This will overwrite your saved settings back to the default values. Any current settings will be lost. Proceed?"
        self.show_confirmation_dialog(title, text, self.reset_settings)

    def callback_block_menu(self, item):
        print(item)
        item_string = item.replace("_", " ").title()
        self.root.ids.block_drop_down.text = item_string
        Settings.current_settings["building_block_choice"] = item

    def callback_switch_theme(self):
        print("Switching Mode!")
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        Settings.set_setting("theme_style", self.theme_cls.theme_style)

    def callback_build_places(self):
        print("Building!")
        try:
            self.builder.build_place(
                self.loaded_reference,
                self.loaded_build_places,
                Settings.current_settings["base_building_height"],
                Settings.current_settings["building_block_choice"],
                Settings.current_settings["scaling_factor"],
            )

            parser = PlaceParser()
            for file in self.loaded_build_places:
                found_place = parser.parse_place(file)[0]
                item = OneLineListItem(text=found_place.name)
                self.root.ids.build_history_list.add_widget(item)

        except AutomationException as e:
            print(f"ERROR: {e.message}")
            self.show_alert_dialog(f"Automation has been halted. {e.message}")

        self.window_manager.set_current_window(self.window_manager.find_window(self.app_name)[0])

    def load_reference(self, reference_file_path):
        parser = PlaceParser()
        if not reference_file_path:
            self.show_alert_dialog("You must select at one file for the automation to use as a reference point.")
        else:
            print(reference_file_path)
            Settings.set_setting("last_used_reference", reference_file_path)
            self.loaded_reference = parser.parse_place(reference_file_path)[0]
            ref_coords = self.loaded_reference.coordinate_list[0]
            print(self.loaded_reference.name)
            print(ref_coords)

            name_string = f"[b]Name:[/b] {self.loaded_reference.name}\n"
            latitude_string = f"[b]Latitude:[/b] {round(degrees(ref_coords.latitude), 6)}°\n"
            longitude_string = f"[b]Longitude:[/b] {round(degrees(ref_coords.longitude), 6)}°"
            info_string = name_string + latitude_string + longitude_string
            self.root.ids.reference_information.text = info_string

            self.window_manager.set_current_window(self.window_manager.find_window(self.app_name)[0])

    def callback_update_game_version(self, show_error=True):
        print("Attempting to find game version")
        try:
            automator = GameAutomator()
            version = automator.find_minecraft_version()
            print("Found version: " + version)
            self.root.ids.minecraft_version_label.text = version
            Settings.set_setting("last_used_game_version", version)
        except AutomationException:
            print("No Game Version Found, Defaulting to 1.18")
            self.root.ids.minecraft_version_label.text = "1.18"
            Settings.set_setting("last_used_game_version", "1.18")
            if show_error:
                self.show_alert_dialog("No Game Window was found. Defaulting to Minecraft Version 1.18")

    def callback_load_reference_place(self):
        print("Loading Reference Places!")
        reference_file_path = filedialog.askopenfilename()
        self.load_reference(reference_file_path)

    def callback_load_build_places(self):
        print("Loading Build Places!")
        parser = PlaceParser()
        places_file_paths = filedialog.askopenfilenames()
        if not places_file_paths:
            self.show_alert_dialog("You must select at least one file for you to build.")
        else:
            self.root.ids.loaded_places_list.clear_widgets()
            self.loaded_build_places = places_file_paths
            print(places_file_paths)
            for file in places_file_paths:
                found_place = parser.parse_place(file)[0]
                color = color_to_minecraft_dye(found_place.color).replace("_", " ").title()
                num_points = len(found_place.coordinate_list)
                item = ThreeLineListItem(
                    text=f"{found_place.name}", secondary_text=f"Color: {color}", tertiary_text=f"Corners: {num_points}"
                )
                self.root.ids.loaded_places_list.add_widget(item)
            self.window_manager.set_current_window(self.window_manager.find_window(self.app_name)[0])

    def callback_slide_scale(self, *args):
        scale = int(args[1])
        self.root.ids.scale_label.text = f"{scale}%"
        Settings.set_setting("scaling_factor", scale / 100.0)

    def callback_slide_y(self, *args):
        y = int(args[1])
        self.root.ids.base_y_label.text = f"{y}"
        Settings.set_setting("base_building_height", y)


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
    Settings.save_settings()
