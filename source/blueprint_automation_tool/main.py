import window
from builder import PlaceBuilder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp


# Declare Screens
class Screen1(Screen):
    pass


class Screen2(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.app_name = "Blueprint Automation Tool"

        self.title = self.app_name
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name="screen1"))
        self.sm.add_widget(Screen2(name="screen2"))

        return self.sm

    def change_screen(self, screen):
        self.sm.current = screen

    def build_places(self):
        b = PlaceBuilder()
        w = window.WindowHandler()
        b.build_place()
        w.set_current_window(w.find_window(self.app_name)[0])


MainApp().run()
