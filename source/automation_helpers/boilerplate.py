"""
File:
Description:

Author:
"""

# pylint: disable-all
import ctypes
from ctypes import wintypes
from time import sleep

import win32con

user32 = ctypes.WinDLL('user32', use_last_error=True)

# C Struct Definitions


class MouseInput(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.WPARAM))


class KeyboardInput(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.WPARAM))

    def __init__(self, *args, **kwds):
        super(KeyboardInput, self).__init__(*args, **kwds)
        if not self.dwFlags & win32con.KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, 0, 0)


class HardwareInput(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class Input(ctypes.Structure):
    class _Input(ctypes.Union):
        _fields_ = (("ki", KeyboardInput),
                    ("mi", MouseInput),
                    ("hi", HardwareInput))
    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _Input))


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(Input), ctypes.c_int)
