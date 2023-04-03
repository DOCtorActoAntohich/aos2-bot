from __future__ import annotations

import string

import cv2
import numpy
import tesserocr
from PIL import Image

from emi.math import Rect
from emi.settings import Settings


class Color:
    White = 255


def crop_rect(image: numpy.ndarray, rect: Rect) -> numpy.ndarray:
    return image[rect.top : rect.bottom, rect.left : rect.right]


def fill_all_contours(mask: numpy.ndarray, contours: list) -> numpy.ndarray:
    cv2.drawContours(mask, contours, -1, Color.White, thickness=-1)
    return mask


def extend(image: numpy.ndarray, x: int, y: int) -> numpy.ndarray:
    original_y, original_x = image.shape
    new_shape = (original_y + y, original_x + x)
    new_image = numpy.zeros(new_shape, dtype=numpy.uint8)
    y_start = y // 2
    y_end = y // 2 + original_y
    x_start = x // 2
    x_end = x // 2 + original_x
    new_image[y_start:y_end, x_start:x_end] = image
    return new_image


class OcrEngine:
    __heat_text_engine: tesserocr.PyTessBaseAPI = None
    __health_text_engine: tesserocr.PyTessBaseAPI = None

    @classmethod
    def for_heat_text(cls) -> tesserocr.PyTessBaseAPI:
        if cls.__heat_text_engine is None:
            cls.__heat_text_engine = tesserocr.PyTessBaseAPI(path=Settings.ocr.data_path)
            cls.__heat_text_engine.SetPageSegMode(tesserocr.PSM.SINGLE_LINE)
            cls.__heat_text_engine.SetVariable("tessedit_char_whitelist", string.digits)
            cls.__heat_text_engine.Init(lang="eng", oem=tesserocr.OEM.LSTM_ONLY, path=Settings.ocr.data_path)
        return cls.__heat_text_engine

    @classmethod
    def for_health_text(cls) -> tesserocr.PyTessBaseAPI:
        if cls.__health_text_engine is None:
            cls.__health_text_engine = tesserocr.PyTessBaseAPI(path=Settings.ocr.data_path)
            cls.__health_text_engine.SetPageSegMode(tesserocr.PSM.SINGLE_LINE)
            cls.__health_text_engine.SetVariable("tessedit_char_whitelist", string.digits + "/")
            cls.__health_text_engine.Init(lang="eng", oem=tesserocr.OEM.LSTM_ONLY, path=Settings.ocr.data_path)
        return cls.__health_text_engine

    @classmethod
    def recognize_text(cls, engine: tesserocr.PyTessBaseAPI, raw_image: numpy.ndarray) -> str:
        text_source = Image.fromarray(raw_image)
        engine.SetImage(text_source)
        return engine.GetUTF8Text().strip() or ""

    @classmethod
    def recognize_heat(cls, raw_image: numpy.ndarray) -> str:
        return cls.recognize_text(cls.for_heat_text(), raw_image)

    @classmethod
    def recognize_health(cls, raw_image: numpy.ndarray) -> str:
        return cls.recognize_text(cls.for_health_text(), raw_image)


class HeatTextContour:
    MinArea = 10
    MaxArea = 3000
    MinAspectRatio = 0.2
    MaxAspectRatio = 1.0

    @classmethod
    def has_suitable_area(cls, area: float) -> bool:
        return cls.MinArea <= area <= cls.MaxArea

    @classmethod
    def has_suitable_aspect_ratio(cls, aspect_ratio: float) -> bool:
        return cls.MinAspectRatio <= aspect_ratio <= cls.MaxAspectRatio


class InterfaceData:
    RedHeatTextGrayscaleThreshold = 105
    HealthTextThreshold = 225
    LettersLikeNumbers = {
        "o": "0",
        "z": "2",
        "s": "5",
        "g": "9",
    }

    def __init__(self, grayscale_frame: numpy.ndarray) -> None:
        self.ui_frame = crop_rect(grayscale_frame, Settings.ui.Position)

    @property
    def p1_heat(self) -> int:
        return self.__get_heat(Settings.ui.p1.HeatPosition)

    @property
    def p2_heat(self) -> int:
        return self.__get_heat(Settings.ui.p2.HeatPosition)

    @property
    def p1_health(self) -> tuple[int, int]:
        return self.__get_health(Settings.ui.p1.HealthPosition)

    @property
    def p2_health(self) -> tuple[int, int]:
        return self.__get_health(Settings.ui.p2.HealthPosition)

    def __get_health(self, health_zone_location: Rect) -> tuple[int, int]:
        health_zone = crop_rect(self.ui_frame, health_zone_location)
        text = self.__recognize_health_text(health_zone)
        return self.__corrected_health(text)

    def __recognize_health_text(self, health_zone: numpy.ndarray) -> str:
        _, binary_image = cv2.threshold(health_zone, self.HealthTextThreshold, 255, cv2.THRESH_BINARY)

        health_zone = extend(binary_image, x=10, y=10)

        return OcrEngine.recognize_health(health_zone)

    def __get_heat(self, heat_zone_location: Rect) -> int:
        heat_zone = crop_rect(self.ui_frame, heat_zone_location)
        text = self.__recognize_heat_text(heat_zone)
        return self.__corrected_heat(text)

    def __recognize_heat_text(self, heat_zone: numpy.ndarray) -> str:
        heat_zone = cv2.fastNlMeansDenoising(heat_zone, None, 10, 7, 21)

        _, binary_image = cv2.threshold(heat_zone, self.RedHeatTextGrayscaleThreshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        small_contours = self.__filter_small_contours(contours)

        mask = fill_all_contours(numpy.zeros(heat_zone.shape, numpy.uint8), small_contours)
        masked_heat_zone = cv2.bitwise_and(heat_zone, heat_zone, mask=mask)

        return OcrEngine.recognize_heat(masked_heat_zone)

    @classmethod
    def __filter_small_contours(cls, contours: list) -> list:
        suitable_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, width, height = cv2.boundingRect(contour)
            aspect_ratio = width / height
            if HeatTextContour.has_suitable_area(area) and HeatTextContour.has_suitable_aspect_ratio(aspect_ratio):
                suitable_contours.append(contour)
        return suitable_contours

    def __corrected_heat(self, raw_text: str) -> int:
        heat_text = self.__correct_text(raw_text)
        return self.__text_to_number(heat_text, Settings.game.MinHeat, Settings.game.MaxHeat)

    def __corrected_health(self, raw_text: str) -> tuple[int, int]:
        health_text = self.__correct_text(raw_text, extra_characters="/")
        try:
            left, right = health_text.split("/", maxsplit=1)
        except ValueError:
            return -1, -1

        return (
            self.__text_to_number(left, Settings.game.MinHealth, Settings.game.MaxHealth),
            self.__text_to_number(right, Settings.game.MinHealth, Settings.game.MaxHealth),
        )

    @classmethod
    def __text_to_number(cls, text: str, min_value: int, max_value: int) -> int:
        try:
            number = int(text)
        except ValueError:
            return -1

        if not min_value <= number <= max_value:
            return -1

        return number

    def __correct_text(self, raw_text: str, *, extra_characters: str = "") -> str:
        corrected_text = ""
        for character in raw_text.lower():
            if character.isdigit() or character in extra_characters:
                corrected_text += character
            if character in self.LettersLikeNumbers:
                corrected_text += self.LettersLikeNumbers[character]
        return corrected_text
