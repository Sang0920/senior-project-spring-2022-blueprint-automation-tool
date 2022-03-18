"""
File:           window.py
Description:    handles window automation on Windows Automation

Author(s):      Kevin Green
Last Revised:   24 Feb 2022
"""

# Built-In Modules
import re
import time

# Installed Modules
import win32com.client
import win32con
import win32gui


class WindowHandler:
    def _get_all_windows(self):
        """Gets visible named windows that are open on the host system.

        Returns:
            The of windows that were found.

        """

        def _callback(hwnd, context):
            if win32gui.IsWindowVisible(hwnd):  # Makes sure that the window is visible
                if (
                    win32gui.GetWindowText(hwnd) != ""
                ):  # Makes sure the window has a title
                    context.append(Window(hwnd))

        windows_list = []
        win32gui.EnumWindows(_callback, windows_list)
        return windows_list

    def find_window(self, title, limit=None):
        """Finds all windows whose titles match the regex given.

        Args:
            title : Regex string for the window that is being located.
            limit : The maximum number of windows to return. Forces the function to return the first n windows.

        Returns:
            A list of windows that matched the title regex.
        """
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
        """Gets the currently active window that is in the foreground of the system.

        Returns:
            Window object of the currently active window.
        """
        hwnd = win32gui.GetForegroundWindow()
        return Window(hwnd)

    def set_current_window(self, window):
        """Sets the given window to the active window for the system.

        Args:
            window: Window that should be set as the current window.
        """
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(window.hwnd)
        window.refresh_info()

    def move_window(self, window, x, y):
        """Moves the given window to the given coordinates

        Args:
            window: The window to be moved
            x: The x location for the top-left corner of the window
            y: The y location for the top-left corner of the window
        """
        win32gui.MoveWindow(
            window.hwnd, x - 7, y - 7, window.width, window.height, True
        )
        window.refresh_info()

    def resize_window(self, window, width, height):
        """Resizes the given window to the given dimensions

        Args:
            window: The window to be resized
            width: The new width of the window
            height: The new height of the window
        """
        win32gui.MoveWindow(
            window.hwnd,
            window.coordinates[0],
            window.coordinates[1],
            width,
            height,
            True,
        )
        window.refresh_info()

    def maximize_window(self, window):
        """Maximizes the given window

        Args:
            window: The window to maximize
        """
        win32gui.ShowWindow(window.hwnd, win32con.SW_MAXIMIZE)
        window.refresh_info()

    def minimize_window(self, window):
        """Minimizes the given window

        Args:
            window: The window to minimize
        """
        win32gui.ShowWindow(window.hwnd, win32con.SW_MINIMIZE)
        window.refresh_info()

    def close_window(self, window):
        """Close the given window entirely

        Args:
            window: The window to close
        """
        win32gui.PostMessage(window.hwnd, win32con.WM_CLOSE, 0, 0)
        window.refresh_info()


class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.title = None
        self.coordinates = None
        self.width = None
        self.height = None
        self.refresh_info()

    def refresh_info(self):
        """Gets the most updated information for a window"""
        self.title = win32gui.GetWindowText(self.hwnd)
        self.coordinates = win32gui.GetWindowRect(self.hwnd)
        self.width = self.coordinates[2] - self.coordinates[0]
        self.height = self.coordinates[3] - self.coordinates[1]


# Temporary Testing During Development
if __name__ == "__main__":
    windows = WindowHandler().find_window(".*Visual Studio Code.*")
    for wndw in windows:
        print(wndw.title)

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
