import numpy
import win32gui
import win32ui
import win32con

from emi.math import Vector2, Rect


class Window:
    def __init__(self, window_name: str):
        self.__handle = win32gui.FindWindow(None, window_name)
        if self.__handle == 0:
            raise ValueError(f"Window not found: {window_name}")

        self.update()

    def update(self):
        self.__update_size()
        self.__update_borders()
        self.__capture_new_frame()

    @property
    def size(self) -> Vector2:
        return self.__size

    @property
    def borders_offset(self):
        return self.__borders

    @property
    def last_frame(self) -> numpy.ndarray:
        return self.__last_frame

    def __update_size(self):
        client_rect = Rect.from_tuple(win32gui.GetClientRect(self.__handle))
        self.__size = Vector2(client_rect.width, client_rect.height)

    def __update_borders(self) -> None:
        window_rect = Rect.from_tuple(win32gui.GetWindowRect(self.__handle))
        border_width = (window_rect.width - self.size.x) // 2
        top_bar_height = window_rect.height - border_width - self.size.y
        self.__borders = Vector2(border_width, top_bar_height)

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

        # for opencv.
        signed_ints_array = data_bit_map.GetBitmapBits(True)  # so true...
        img = numpy.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (self.size.y, self.size.x, 4)  # intended swap because numpy

        dc_object.DeleteDC()
        compatible_dc.DeleteDC()
        win32gui.ReleaseDC(self.__handle, window_dc)
        win32gui.DeleteObject(data_bit_map.GetHandle())

        # drop the alpha channel + avoid errors.
        self.__last_frame = numpy.ascontiguousarray(img[..., :3])
