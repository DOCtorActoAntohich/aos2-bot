import ctypes
import ctypes.wintypes
import sys
import threading
from typing import Callable

import win32con

WindowsEventHookCallbackType = Callable[[int, int, int, int, int, int, int], None]


class WindowsHookListenerThread(threading.Thread):
    def __init__(self, callback: WindowsEventHookCallbackType) -> None:
        super().__init__(daemon=True)
        self.hook_handle = 0
        self.callback = callback

    def run(self) -> None:
        # Type must be this
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wineventproc
        void_type = None
        win_event_proc_type = ctypes.WINFUNCTYPE(
            void_type,
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.HWND,
            ctypes.wintypes.LONG,
            ctypes.wintypes.LONG,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
        )
        win_event_proc = win_event_proc_type(self.callback)

        ctypes.windll.user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        hook = ctypes.windll.user32.SetWinEventHook(
            win32con.EVENT_SYSTEM_FOREGROUND,
            win32con.EVENT_SYSTEM_FOREGROUND,
            0,
            win_event_proc,
            0,
            0,
            win32con.WINEVENT_OUTOFCONTEXT,
        )

        if hook == 0:
            sys.exit("Failed to SetWinEventHook")

        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
            ctypes.windll.user32.TranslateMessageW(msg)
            ctypes.windll.user32.DispatchMessageW(msg)

    def __del__(self) -> None:
        if self.hook_handle != 0:
            ctypes.windll.user32.UnhookWinEvent(self.hook_handle)
