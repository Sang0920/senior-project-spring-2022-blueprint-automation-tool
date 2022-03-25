import win32api
import win32con

print(win32api.GetAsyncKeyState(win32con.VK_CAPITAL))
