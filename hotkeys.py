from functools import reduce
from typing import Callable, Optional
import win32gui
import win32con
import time


class Hotkeys:
    "Wrapper for Win32 thread-specific keys"

    registered_keys: dict[int, Callable] = {}
    last_id: int = 0

    def __init__(self):
        return

    def add_hotkey(
        self,
        key: int,
        callback: Callable,
        modifiers: Optional[list[int]] = None,
    ) -> int:
        mod = reduce(lambda a, b: a | b, modifiers, 0) if modifiers else 0
        win32gui.RegisterHotKey(None, self.last_id, mod, key)
        self.registered_keys[self.last_id] = callback
        # this will crash after 2^31 hotkeys
        self.last_id += 1
        return self.last_id - 1

    def remove_hotkey(self, hotkey_id: int):
        if hotkey_id not in self.registered_keys:
            raise ValueError("hotkey_id has not been registered yet")
        del self.registered_keys[hotkey_id]
        win32gui.UnregisterHotKey(None, hotkey_id)

    def poll_messages(self):
        """Uses PeekMessage() to poll for messages without blocking. This
        function will peek messages until none are returned, and thus may
        process multiple messages at once."""
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-msg
        # msg: (hwnd, message, wParam, lParam, time, pt, lPrivate)
        while (res := win32gui.PeekMessage(0, 0, 0, win32con.PM_REMOVE)) and res[0]:
            # https://github.com/python/cpython/issues/87309 :(
            msg = res[1]

            if msg[1] != win32con.WM_HOTKEY:
                return

            # https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-hotkey
            # wParam: identifier of the hot key that generated the message
            hotkey_id = msg[2]
            self.registered_keys[hotkey_id]()

    def poll_loop(self):
        "Loop for poll_messages."
        while True:
            self.poll_messages()
            time.sleep(0.01)
