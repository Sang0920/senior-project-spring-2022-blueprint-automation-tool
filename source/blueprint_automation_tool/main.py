import window
from builder import PlaceBuilder
from game_automation import AutomationException
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog


# Declare Screens
class Screen1(Screen):
    pass


class Screen2(Screen):
    pass


class Screen3(Screen):
    pass


class MainApp(MDApp):
    dialog = None

    def build(self):
        self.app_name = "Blueprint Automation Tool"

        self.title = self.app_name
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name="screen1"))
        self.sm.add_widget(Screen2(name="screen2"))
        self.sm.add_widget(Screen3(name="screen3"))

        return self.sm

    def change_screen(self, screen):
        self.sm.current = screen

    def build_places(self):
        b = PlaceBuilder()
        w = window.WindowHandler()
        try:
            b.build_place()
        except AutomationException as e:
            print(e.message)
            self.show_error_dialog(e.message)
        w.set_current_window(w.find_window(self.app_name)[0])

    def show_error_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Error",
                text=f"{message}",
                buttons=[
                    MDRaisedButton(text="OK", on_release=self.close_error_dialog),
                ],
            )
        self.dialog.open()

    def close_error_dialog(self, obj):
        self.dialog.dismiss()


MainApp().run()
