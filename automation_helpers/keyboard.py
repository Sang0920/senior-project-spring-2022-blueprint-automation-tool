import win32con
import win32api
import win32clipboard
import time

class KeyboardException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KeyboardHandler:

    def __init__(self):
        # TODO: Add missing keys, find more elegant method (YAML file?)
        self.keys = {
            "backspace": 0x08,
            "tab": 0x09,
            "enter": 0x0d,
            "shift": 0x10,
            "ctrl": 0x11,
            "alt": 0x12,
            "capslock": 0x14,
            "escape": 0x1b,
            "spacebar": 0x20,
            " ": 0x20,
            "pageup": 0x21,
            "pagedown": 0x22,
            "end": 0x23,
            "home": 0x24,
            "leftarrow": 0x25,
            "uparrow": 0x26,
            "rightarrow": 0x27,
            "downarrow": 0x28,
            "prtscrn": 0x2c,
            "insert": 0x2d,
            "delete": 0x2e,
            "help": 0x2f,
            "0": 0x30,
            "1": 0x31,
            "2": 0x32,
            "3": 0x33,
            "4": 0x34,
            "5": 0x35,
            "6": 0x36,
            "7": 0x37,
            "8": 0x38,
            "9": 0x39,
            "a": 0x41,
            "b": 0x42,
            "c": 0x43,
            "d": 0x44,
            "e": 0x45,
            "f": 0x46,
            "g": 0x47,
            "h": 0x48,
            "i": 0x49,
            "j": 0x4a,
            "k": 0x4b,
            "l": 0x4c,
            "m": 0x4d,
            "n": 0x4e,
            "o": 0x4f,
            "p": 0x50,
            "q": 0x51,
            "r": 0x52,
            "s": 0x53,
            "t": 0x54,
            "u": 0x55,
            "v": 0x56,
            "w": 0x57,
            "x": 0x58,
            "y": 0x59,
            "z": 0x5a,
            "lwin": 0x5b,
            "rwin": 0x5c,
            "apps": 0x5d,
            "sleep": 0x5f,
            "num0": 0x60,
            "num1": 0x61,
            "num2": 0x62,
            "num3": 0x63,
            "num4": 0x64,
            "num5": 0x65,
            "num6": 0x66,
            "num7": 0x67,
            "num8": 0x68,
            "num9": 0x69,
        }

    def _translate_key(self, key_str):
        if key_str in self.keys:
            return self.keys[key_str]
        else:
            raise KeyboardException(f"Given key {key_str} not found.")

    def press_key(self, key):
        hex_key = self._translate_key(key)
        win32api.keybd_event(hex_key, 0, 0, 0)

    def release_key(self, key):
        hex_key = self._translate_key(key)
        win32api.keybd_event(hex_key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def press_and_release_key(self, key, hold_time = 0):
        self.press_key(key)
        time.sleep(hold_time)
        self.release_key(key)

    def write(self, message, hold_time = 0, pause_between = 0):
        for key in message:
            self.press_and_release_key(key, hold_time)
            time.sleep(pause_between)

    def copy(self):
        # Press Ctrl+C
        self.press_key('ctrl')
        self.press_key('c')
        self.release_key('c')
        self.release_key('ctrl')

        # Get clipboard data and return
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        return data

    def paste(self, text):
        # Set clipboard data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

        # Press Ctrl+V
        self.press_key('ctrl')
        self.press_key('v')
        self.release_key('v')
        self.release_key('ctrl')


KeyboardHandler().paste("test")
KeyboardHandler().press_and_release_key('t')
KeyboardHandler().write("test2")
