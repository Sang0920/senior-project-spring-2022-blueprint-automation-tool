"""
File:           keyboard.py
Description:    handles keyboard automation for Windows

Author(s):      Kevin Green
"""

# Built-In Modules
from time import sleep

# Installed Modules
import ctypes
import win32clipboard
import win32con
from ctypes import wintypes

# pylint: disable=relative-beyond-top-level
from .boilerplate import Input, KeyboardInput, user32

class KeyboardException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class KeyboardHandler:
    def __init__(self):

        # Vk codes to convert strings to hex
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        self.keys = {
            'backspace':    win32con.VK_BACK,
            'tab':          win32con.VK_TAB,
            'clear':        win32con.VK_CLEAR,
            'enter':        win32con.VK_RETURN,
            'shift':        win32con.VK_SHIFT,
            'ctrl':         win32con.VK_CONTROL,
            'alt':          win32con.VK_MENU,
            'pause':        win32con.VK_PAUSE,
            'caps_lock':    win32con.VK_CAPITAL,
            'esc':          win32con.VK_ESCAPE,
            'spacebar':     win32con.VK_SPACE,
            'page_up':      win32con.VK_PRIOR,
            'page_down':    win32con.VK_NEXT,
            'end':          win32con.VK_END,
            'home':         win32con.VK_HOME,
            'left':         win32con.VK_LEFT,
            'up':           win32con.VK_UP,
            'right':        win32con.VK_RIGHT,
            'down':         win32con.VK_DOWN,
            'select':       win32con.VK_SELECT,
            'print':        win32con.VK_PRINT,
            'execute':      win32con.VK_EXECUTE,
            'print_screen': win32con.VK_SNAPSHOT,
            'insert':       win32con.VK_INSERT,
            'delete':       win32con.VK_DELETE,
            'help':         win32con.VK_HELP,
            'l_win':        win32con.VK_LWIN,
            'r_win':        win32con.VK_RWIN,
            'apps':         win32con.VK_APPS,
            'num0':         win32con.VK_NUMPAD0,
            'num1':         win32con.VK_NUMPAD1,
            'num2':         win32con.VK_NUMPAD2,
            'num3':         win32con.VK_NUMPAD3,
            'num4':         win32con.VK_NUMPAD4,
            'num5':         win32con.VK_NUMPAD5,
            'num6':         win32con.VK_NUMPAD6,
            'num7':         win32con.VK_NUMPAD7,
            'num8':         win32con.VK_NUMPAD8,
            'num9':         win32con.VK_NUMPAD9,
            'multiply':     win32con.VK_MULTIPLY,
            'add':          win32con.VK_ADD,
            'separator':    win32con.VK_SEPARATOR,
            'subtract':     win32con.VK_SUBTRACT,
            'decimal':      win32con.VK_DECIMAL,
            'divide':       win32con.VK_DIVIDE,
            'f1':           win32con.VK_F1,
            'f2':           win32con.VK_F2,
            'f3':           win32con.VK_F3,
            'f4':           win32con.VK_F4,
            'f5':           win32con.VK_F5,
            'f6':           win32con.VK_F6,
            'f7':           win32con.VK_F7,
            'f8':           win32con.VK_F8,
            'f9':           win32con.VK_F9,
            'f10':          win32con.VK_F10,
            'f11':          win32con.VK_F11,
            'f12':          win32con.VK_F12,
            'f13':          win32con.VK_F13,
            'f14':          win32con.VK_F14,
            'f15':          win32con.VK_F15,
            'f16':          win32con.VK_F16,
            'f17':          win32con.VK_F17,
            'f18':          win32con.VK_F18,
            'f19':          win32con.VK_F19,
            'f20':          win32con.VK_F20,
            'f21':          win32con.VK_F21,
            'f22':          win32con.VK_F22,
            'f23':          win32con.VK_F23,
            'f24':          win32con.VK_F24,
            'num_lock':     win32con.VK_NUMLOCK,
            'scroll_lock':  win32con.VK_SCROLL,
            'l_shift':      win32con.VK_LSHIFT,
            'r_shift':      win32con.VK_RSHIFT,
            'l_ctrl':       win32con.VK_LCONTROL,
            'r_ctrl':       win32con.VK_RCONTROL,
            'l_alt':        win32con.VK_LMENU,
            'r_alt':        win32con.VK_RMENU,
            'mute':         win32con.VK_VOLUME_MUTE,
            'volume_down':  win32con.VK_VOLUME_DOWN,
            'volume_up':    win32con.VK_VOLUME_UP,
        }

        # generate conversion from ascii chars to VK codes
        for i in range(32, 128):
            self.keys[chr(i)] = ctypes.windll.user32.VkKeyScanA(wintypes.WCHAR(chr(i)))

    def _translate_key(self, key):
        if key in self.keys:
            return self.keys[key]
        else:
            raise KeyboardException(f"Given key {key} not found.")

    def press(self, key):
        hex_key = self._translate_key(key)
        x = Input(type=1, ki=KeyboardInput(wVk=hex_key))
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    def release(self, key):
        hex_key = self._translate_key(key)
        x = Input(type=1, ki=KeyboardInput(wVk=hex_key, dwFlags=win32con.KEYEVENTF_KEYUP))
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    def press_and_release(self, key, hold_time=0.1):
        self.press(key)
        sleep(hold_time)
        self.release(key)

    def write(self, message, hold_time=0.1, pause_between=0.1):
        for key in message:
            self.press_and_release(key, hold_time)
            sleep(pause_between)

    def copy(self):
        # Press Ctrl+C
        self.press('ctrl')
        self.press('c')
        self.release('c')
        self.release('ctrl')

        # Get clipboard data and return
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data

    def paste(self, text):
        # Set clipboard text
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

        # Press Ctrl+V
        self.press('ctrl')
        self.press('v')
        self.release('v')
        self.release('ctrl')

# print(KeyboardHandler().keys)
# KeyboardHandler().paste("test")
# KeyboardHandler().write("test2")
