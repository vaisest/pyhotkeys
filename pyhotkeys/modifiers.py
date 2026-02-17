# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerhotkey

# Either ALT key must be held down.
MOD_ALT = 0x1
# Either CTRL key must be held down.
MOD_CONTROL = 0x2
# Changes the hotkey behavior so that the keyboard auto-repeat does not yield
# multiple hotkey notifications. Windows Vista: This flag is not supported.
MOD_NOREPEAT = 0x4000
# Either SHIFT key must be held down.
MOD_SHIFT = 0x0004
# # Either WINDOWS key must be held down. These keys are labeled with the Windows logo. Keyboard shortcuts that involve the WINDOWS key are reserved for use by the operating system.
# MOD_WIN = 0x0008
