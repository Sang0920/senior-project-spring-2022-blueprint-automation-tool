"""
File:           window.py
Description:    handles window automation on Windows Automation

Author(s):      Kevin Green
Last Revised:   11 Feb 2022
"""

# Built-In Modules
import re
import time

# Installed Modules
import win32con
import win32gui

class WindowHandler:
    def _get_all_windows(self):
        def _callback(hwnd, context):
            if win32gui.IsWindowVisible(hwnd):  # Makes sure that the window is visible
                if win32gui.GetWindowText(hwnd) != "":  # Makes sure the window has a title
                    context.append(Window(hwnd))

        windows = []
        win32gui.EnumWindows(_callback, windows)
        return windows

    def find_window(self, title, limit=None):
        # Returns all windows that match the title
        # If a limit is set, it will return the first n of these windows that are found
        found_windows = []
        num_found = 0
        available_windows = self._get_all_windows()
        for window in available_windows:
            if re.search(title, window.title):
                found_windows.append(window)
                num_found += 1
                if limit and num_found >= limit:
                    return found_windows
        return found_windows

    def get_current_window(self):
        hwnd = win32gui.GetForegroundWindow()
        return Window(hwnd)

    def set_current_window(self, window):
        win32gui.SetForegroundWindow(window.hwnd)
        window.refresh_info()

    def move_window(self, window, x, y):
        win32gui.MoveWindow(window.hwnd, x - 7, y - 7, window.width, window.height, True)
        window.refresh_info()

    def resize_window(self, window, width, height):
        win32gui.MoveWindow(window.hwnd, window.coordinates[0], window.coordinates[1], width, height, True)
        window.refresh_info()

    def maximize_window(self, window):
        win32gui.ShowWindow(window.hwnd, win32con.SW_MAXIMIZE)

    def minimize_window(self, window):
        win32gui.ShowWindow(window.hwnd, win32con.SW_MINIMIZE)

    def close_window(self, window):
        win32gui.PostMessage(window.hwnd, win32con.WM_CLOSE, 0, 0)

class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.title = None
        self.coordinates = None
        self.width = None
        self.height = None
        self.refresh_info()

    def refresh_info(self):
        self.title = win32gui.GetWindowText(self.hwnd)
        self.coordinates = win32gui.GetWindowRect(self.hwnd)
        self.width = self.coordinates[2] - self.coordinates[0]
        self.height = self.coordinates[3] - self.coordinates[1]

if __name__ == "__main__":
    WindowHandler()._get_all_windows()
    windows = WindowHandler().find_window(".*Visual Studio Code.*")
    for window in windows:
        print(window.title)

    print(WindowHandler().get_current_window().title)

    windows = WindowHandler().find_window(".*OneNote.*")
    WindowHandler().set_current_window(windows[0])
    WindowHandler().move_window(windows[0], 0, 0)
    WindowHandler().resize_window(windows[0], 1920, 1080)
    time.sleep(2)
    WindowHandler().minimize_window(windows[0])
    time.sleep(1)
    WindowHandler().maximize_window(windows[0])
    time.sleep(2)
    WindowHandler().close_window(windows[0])
