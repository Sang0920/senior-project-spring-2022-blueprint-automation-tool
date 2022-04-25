"""
File:           __main__.py
Description:    Defines main functions and GUI interactions for the application
"""

import os
import sys
import tkinter as tk
from math import degrees
from tkinter import filedialog

import builder
import color_matcher
import constants
import game_automation
import place_parser
import settings
import window
from kivy.clock import Clock, mainthread
from kivy.config import Config
from kivy.lang import Builder
from kivy.logger import LOG_LEVELS, Logger
from kivy.metrics import dp
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("kivy", "log_dir", constants.LOGS_PATH)
Config.set("kivy", "log_name", "kivy_%y-%m-%d_%_.txt")
Config.set("kivy", "log_enable", 1)
Logger.setLevel(LOG_LEVELS["debug"])

Settings = settings.SettingsManager()


class Content(BoxLayout):
    pass


class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        """Called before the application is built"""

        super().__init__(**kwargs)

        # Settings reference by UI and automation
        self.loaded_reference = None
        self.loaded_build_obj = None
        self.window_manager = window.WindowHandler()

        # Main Screen for the application
        self.screen = Builder.load_file("main.kv")

        # Menu Options
        Logger.debug("Main: Creating menu items for block drop down")
        block_menu_items = []
        for block in constants.BLOCKS:
            formatted_name = block.replace("_", " ").title()
            new_item = {
                "text": formatted_name,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=block: self.on_block_menu_update(x),
            }
            block_menu_items.append(new_item.copy())
        Logger.debug(f"Main: Block Menu Items: {block_menu_items}")

        # Dynamically Created Widgets
        self.dialog = None
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.block_drop_down,
            items=block_menu_items,
            width_mult=4,
        )

    def build(self):
        """Called as the application is being built

        Returns:
            The built application
        """

        # Set up theming for the application
        self.title = constants.APPLICATION_NAME
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = Settings.current_settings["theme_style"]
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Amber"

        return self.screen

    def on_start(self):
        """Called immediately after the application is built"""

        self.update_settings_values()
        if Settings.current_settings["last_used_reference"]:
            if os.path.isfile(Settings.current_settings["last_used_reference"]):
                self.load_reference(Settings.current_settings["last_used_reference"])

    # APPLICATION CALLBACKS

    def on_block_menu_update(self, block_type, *args):
        """Called when the user chooses a new block type in the configuration menu

        Args:
            block_type: The Minecraft id for the block
        """

        formatted_block = block_type.replace("_", " ").title()
        Settings.current_settings["building_block_choice"] = block_type
        self.root.ids.block_drop_down.text = formatted_block

    def on_build_places(self, *args):
        """Called when the user chooses to build a new place"""
        Logger.info("Main: Building Places from self.loaded_build_obj")
        try:
            # Build the loaded list of places
            b = builder.PlaceBuilder()
            b.build_places(
                self.loaded_reference,
                self.loaded_build_obj,
                Settings.current_settings["base_building_height"],
                Settings.current_settings["building_block_choice"],
                Settings.current_settings["scaling_factor"],
            )

            # Update the build history to include newly built places
            self.add_places_to_list(self.root.ids.build_history_list, self.loaded_build_obj)

        # Something went wrong with the automation, display an error dialog
        except game_automation.AutomationException as e:
            Logger.error(f"Main: Automation has been halted. {e.message}")
            self.open_alert_dialog(f"Automation has been halted. {e.message}")

        self.return_to_program()
        snackbar = Snackbar(
            text="Automation Complete!",
            snackbar_x=dp(10),
            snackbar_y=dp(10),
            size_hint_x=0.7,
            duration=15,
        )
        snackbar.buttons = [
            MDFlatButton(
                text="OK",
                on_release=snackbar.dismiss,
            )
        ]
        snackbar.open()

    def on_detect_minecraft_version(self, show_error=True, *args):
        """Called when the application needs to detect the game version. Updates corresponding
            labels and settings.

        Args:
            show_error: Whether to show the alert dialog if detection fails. Defaults to True.
        """

        try:
            # Get the minecraft version
            automator = game_automation.GameAutomator()
            version = automator.find_minecraft_version()

            # Update the settings
            Settings.set_setting("last_used_game_version", version)

            # Update widgets
            self.root.ids.minecraft_version_label.text = version
            self.root.ids.height_value_slider.min = automator.min_height
            self.root.ids.height_value_slider.max = automator.max_height + 1

        # No minecraft version was found
        except game_automation.AutomationException:
            Logger.error("Main: Minecraft not found. Defaulting to version 1.18")

            # Update with default version
            Settings.set_setting("last_used_game_version", "1.18")

            # Update widgets
            self.root.ids.minecraft_version_label.text = "1.18"
            self.root.ids.height_value_slider.min = -64
            self.root.ids.height_value_slider.max = 320

            # Show an error, if desired
            if show_error:
                self.open_alert_dialog("Minecraft not found. Defaulting to Minecraft version 1.18")

    def on_load_places(self, *args):
        """Called when the user chooses to load places to build"""
        self.dialog = MDDialog(
            title="Processing...",
            text="Please wait while the places are being loaded.",
        )
        self.dialog.open()

        Clock.schedule_once(lambda dt: self.load_places_task(), 0)

        self.dismiss()

    def load_places_task(self):
        """Gets .kml/.kmz files to build from the user"""
        # Prompt user to load files
        root = tk.Tk()
        root.withdraw()
        place_paths = filedialog.askopenfilenames(
            title="Select The Files That You Would Like To Build",
            filetypes=[("KML Files", "*.kml"), ("KMZ Files", "*.kmz")],
        )
        self.return_to_program()

        # Update loaded places if some were chosen
        self.loaded_build_obj = []
        if place_paths:
            parser = place_parser.PlaceParser()
            for file in place_paths:
                found_places = parser.parse_place(file)
                for p in found_places:
                    self.loaded_build_obj.append(p)
            self.root.ids.loaded_places_list.clear_widgets()
            self.add_places_to_list(self.root.ids.loaded_places_list, self.loaded_build_obj)

    def on_load_reference(self, *args):
        """Called when the user chooses to load a reference file"""
        self.dialog = MDDialog(
            title="Processing...",
            text="Please wait while the reference is being loaded.",
        )
        self.dialog.open()

        Clock.schedule_once(lambda dt: self.load_reference_task(), 0)

        self.dismiss()

    def load_reference_task(self):
        """Gets .kml/.kmz files to use as a reference from the user"""
        # Prompt User to select a reference file
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Select A File To Use As The Central Reference Point",
            filetypes=[("KML Files", "*.kml"), ("KMZ Files", "*.kmz")],
        )
        self.return_to_program()

        # Update loaded reference place if one was chosen
        if path and os.path.isfile(path):
            self.load_reference(path)

    def on_reset_settings(self, *args):
        """Called when the user chooses to reset the application settings"""

        self.open_confirmation_dialog("Reset Settings?", "Are you sure?", self.reset_settings)

    def on_darkmode_toggle(self, switch, value, *args):
        """Called when the user toggles the dark mode switch

        Args:
            switch: The switch widget that was toggled
            value: The value that the switch was set to
        """

        if value:
            self.theme_cls.theme_style = "Dark"
            Settings.set_setting("theme_style", "Dark")
        else:
            self.theme_cls.theme_style = "Light"
            Settings.set_setting("theme_style", "Light")

    def on_slider_change(self, slider, textfield, setting, *args):
        """Called when the user updates a slider

        Args:
            slider: The slider widget that was updated
            textfield: The corresponding text field widget
            setting: The setting that should be updated
        """

        value = int(args[1])
        textfield.text = f"{value}"

        if setting == "scaling_factor":
            value = value / 100.0

        Settings.set_setting(setting, value)

    def on_textfield_change(self, slider, textfield, setting, *args):
        """Called when the user updates a text field

        Args:
            slider: The corresponding slider widget
            textfield: The text field widget that was updated
            setting: The setting that should be updated
        """

        if args[1] and args[1] != "-":
            value = int(args[1])

            # Check to make sure that the new value is within the slider's bounds
            if value >= slider.min and value <= slider.max:
                slider.value = value

                if setting == "scaling_factor":
                    value = value / 100.0

                Settings.set_setting(setting, value)

    # DIALOG FUNCTIONS

    def open_alert_dialog(self, text):
        """Opens a dialog box that shows the user an alert

        Args:
            text: The message to display to the user
        """

        Logger.warn(f"Main: {text}")

        self.dialog = MDDialog(
            title="Alert!",
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=self.dismiss),
            ],
        )
        self.dialog.open()

    def open_confirmation_dialog(self, title, text, callback):
        """Opens a dialog box that asks the user to confirm their decision

        Args:
            title: Title to display on the box
            text: The message to display to the user
            callback: The function to run if the user confirms their decision
        """

        Logger.info(f"Main: {title}: {text}")

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="Confirm", on_release=callback),
                MDFlatButton(text="Cancel", on_release=self.dismiss),
            ],
        )
        self.dialog.open()

    @mainthread
    def dismiss(self, *args):
        """Dismisses the currently active dialog box"""
        Logger.debug("Dismissing Current Dialog")
        self.dialog.dismiss()

    # APPLICATION FUNCTIONALITY

    def add_places_to_list(self, list, places):
        """Adds a list of places to a list widget

        Args:
            list: The list widget to add places too
            places: The list of places to add
        """

        Logger.info("Main: Addding places to list")

        # Parse the loaded places files and add them to the list
        for p in self.loaded_build_obj:
            color = color_matcher.color_to_minecraft_dye(p.color).replace("_", " ").title()
            num_points = len(p.coordinate_list)
            item = ThreeLineListItem(
                text=p.name,
                secondary_text=f"Color: {color}",
                tertiary_text=f"Corners: {num_points}",
            )
            list.add_widget(item)

        Logger.info("Main: Finished adding places to list")

    def load_reference(self, reference_file_path):
        """Loads a reference file into the application

        Args:
            reference_file_path: The path to the reference file
        """

        Logger.info("Main: Loading Reference File")

        parser = place_parser.PlaceParser()
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

        Logger.info("Main: Reference File Loaded")

    def reset_settings(self, *args):
        """Resets the application settings to their default values"""

        self.dismiss()

        Logger.warn("Main: Resetting Settings to Defaults!")

        Settings.load_defaults()
        self.update_settings_values()

        Logger.info("Main: Finished resetting settings")

    def return_to_program(self, *args):
        """Brings the user back to the program window. Used usually when exiting a file dialog"""
        self.window_manager.set_current_window(
            self.window_manager.find_window(constants.APPLICATION_NAME)[0]
        )

    def update_settings_values(self, *args):
        """Update the widgets in the application to reflect the current settings"""

        Logger.info("Main: Updating Labels")

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

        Logger.info("Main: Finished Updating Labels")


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))

    Logger.info("Main: Starting Application")

    MainApp().run()
    Settings.save_settings()

    Logger.info("Main: Application Closed Successfully")
