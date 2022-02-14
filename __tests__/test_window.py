from .window import WindowHandler

window_manager = WindowHandler()

windows = WindowHandler()._get_all_windows()
for window in windows:
    print(window.title)

windows = WindowHandler().find_window(".*test_window.*")
for window in windows:
    print(window.title)
