from threading import Lock

import numpy
import win32gui
import win32ui
import win32con
import pydirectinput

from emi.math import Vector2, Rect
from emi.windows.hook_listener_thread import WindowsEventHookCallbackType
from emi.bot.controls import Controls


class Window:
    @property
    def focus_change_callback(self) -> WindowsEventHookCallbackType:
        def callback(
                h_win_event_hook: int,
                event: int,
                hwnd: int,
                id_object: int,
                id_child: int,
                event_thread_id: int,
                event_time: int
        ) -> None:
            self.on_focus_change(hwnd)

        return callback

    def __init__(self, window_name: str):
        self.__handle = win32gui.FindWindow(None, window_name)
        if self.__handle == 0:
            raise ValueError(f"Window not found: {window_name}")

        self.__is_active = False
        self.__buttons_control_lock = Lock()
        self.__is_minimized = False
        self.__pressed_buttons: list[Controls] = []

        self.update()

    def update(self) -> None:
        self.__is_minimized = self.__get_minimized()
        if self.__is_minimized:
            return
        self.__update_size()
        self.__update_borders()
        self.__capture_new_frame()

    def on_focus_change(self, foreground_window_handle: int) -> None:
        if foreground_window_handle == self.__handle:
            self.__on_become_foreground()
            return

        self.__on_become_background()

    def set_new_inputs(self, buttons: list[Controls]) -> None:
        with self.__buttons_control_lock:
            self.__all_keys_up()
            self.__pressed_buttons = buttons
            if self.__is_active:
                self.__all_keys_down()

    def __all_keys_down(self):
        for button in self.__pressed_buttons:
            self.__key_down(button.to_key_code())

    def __all_keys_up(self):
        for button in self.__pressed_buttons:
            self.__key_up(button.to_key_code())

    @classmethod
    def __key_down(cls, code: str) -> None:
        pydirectinput.keyDown(code)

    @classmethod
    def __key_up(cls, code: str) -> None:
        pydirectinput.keyUp(code)

    @property
    def is_active(self):
        return self.__is_active

    @property
    def size(self) -> Vector2:
        return self.__size

    @property
    def borders_offset(self):
        return self.__borders

    @property
    def last_frame(self) -> numpy.ndarray:
        return self.__last_frame

    def __get_minimized(self) -> bool:
        _, state, *_ = win32gui.GetWindowPlacement(self.__handle)
        return state == win32con.SW_SHOWMINIMIZED

    def __update_size(self):
        client_rect = Rect.from_tuple(win32gui.GetClientRect(self.__handle))
        self.__size = Vector2(client_rect.width, client_rect.height)

    def __update_borders(self) -> None:
        window_rect = Rect.from_tuple(win32gui.GetWindowRect(self.__handle))
        border_width = (window_rect.width - self.size.x) // 2
        top_bar_height = window_rect.height - border_width - self.size.y
        self.__borders = Vector2(border_width, top_bar_height)

    def __on_become_foreground(self) -> None:
        self.__is_active = True
        with self.__buttons_control_lock:
            self.__all_keys_down()

    def __on_become_background(self) -> None:
        self.__is_active = False
        with self.__buttons_control_lock:
            self.__all_keys_up()

    def __capture_new_frame(self) -> None:
        window_dc = win32gui.GetWindowDC(self.__handle)
        dc_object = win32ui.CreateDCFromHandle(window_dc)
        compatible_dc = dc_object.CreateCompatibleDC()

        data_bit_map = win32ui.CreateBitmap()
        data_bit_map.CreateCompatibleBitmap(dc_object, self.size.x, self.size.y)

        compatible_dc.SelectObject(data_bit_map)
        compatible_dc.BitBlt(
            (0, 0),
            self.size.as_tuple,
            dc_object,
            self.borders_offset.as_tuple,
            win32con.SRCCOPY
        )

        signed_ints_array = data_bit_map.GetBitmapBits(True)  # so true...
        img = numpy.frombuffer(signed_ints_array, dtype=numpy.uint8)
        img.shape = (self.size.y, self.size.x, 4)  # intended order because numpy; in-place.

        dc_object.DeleteDC()
        compatible_dc.DeleteDC()
        win32gui.ReleaseDC(self.__handle, window_dc)
        win32gui.DeleteObject(data_bit_map.GetHandle())

        # drop the alpha channel + avoid errors.
        self.__last_frame = numpy.ascontiguousarray(img[..., :3])
