import win32more.Windows.Win32.UI.Input.KeyboardAndMouse as kbm
import keycodes
from ctypes import sizeof
from win32api import SetCursorPos

# SendInput(cInputs: UInt32, pInputs: POINTER(win32more.Windows.Win32.UI.Input.KeyboardAndMouse.INPUT), cbSize: Int32) -> UInt32
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput


def send_vk_down_up(keycodes: list[int]) -> bool:
    """Sends a list of keycodes (which can include modifiers).
    The key-down actions are first send in order, and
    then the key-up actions are sent in the opposite order."""
    inputs = (kbm.INPUT * (2 * len(keycodes)))()
    # send down inputs in order
    for i, code in enumerate(keycodes):
        inputs[i].type = kbm.INPUT_KEYBOARD
        inputs[i].ki.wVk = code

    # send up inputs in reverse order
    for i, code in enumerate(reversed(keycodes)):
        idx = i + len(keycodes)
        inputs[idx].type = kbm.INPUT_KEYBOARD
        inputs[idx].ki.wVk = code
        inputs[idx].ki.dwFlags = kbm.KEYEVENTF_KEYUP
    return bool(kbm.SendInput(len(inputs), inputs, sizeof(inputs[0])))


def send_vk(keycode: int, up=False) -> bool:
    """Sends a single keycode.
    It should be noted that this only sends a single up or down action."""
    input = kbm.INPUT()
    input.type = kbm.INPUT_KEYBOARD
    input.ki.wVk = keycode
    if up:
        input.ki.dwFlags = kbm.KEYEVENTF_KEYUP
    return bool(kbm.SendInput(1, input, sizeof(input)))

def move_mouse(x: int, y: int):
    "Moves the mouse cursor. Currently this is simply re-exported from pywin32 for convenience."
    SetCursorPos((x, y))


if __name__ == "__main__":
    print(send_vk_down_up([keycodes.VK_MENU, keycodes.VK_CONTROL, keycodes.VK_F8]))
