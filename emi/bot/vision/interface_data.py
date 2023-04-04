from __future__ import annotations

import cv2
import numpy

from emi.bot.vision.ocr_engine import OcrEngine
from emi.bot.vision.opencv_extensions import OpenCvExtensions
from emi.primitives import Rectangle
from emi.settings import Settings


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
        self.ui_frame = OpenCvExtensions.crop(grayscale_frame, Settings.ui.Position)

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

    def __get_health(self, health_zone_location: Rectangle) -> tuple[int, int]:
        health_zone = OpenCvExtensions.crop(self.ui_frame, health_zone_location)
        text = self.__recognize_health_text(health_zone)
        return self.__corrected_health(text)

    def __recognize_health_text(self, health_zone: numpy.ndarray) -> str:
        _, binary_image = cv2.threshold(health_zone, self.HealthTextThreshold, 255, cv2.THRESH_BINARY)

        health_zone = OpenCvExtensions.extend(binary_image, x=10, y=10)

        return OcrEngine.recognize_health(health_zone)

    def __get_heat(self, heat_zone_location: Rectangle) -> int:
        heat_zone = OpenCvExtensions.crop(self.ui_frame, heat_zone_location)
        text = self.__recognize_heat_text(heat_zone)
        return self.__corrected_heat(text)

    def __recognize_heat_text(self, heat_zone: numpy.ndarray) -> str:
        heat_zone = cv2.fastNlMeansDenoising(heat_zone, None, 10, 7, 21)

        _, binary_image = cv2.threshold(heat_zone, self.RedHeatTextGrayscaleThreshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        small_contours = self.__filter_small_contours(contours)

        mask = OpenCvExtensions.fill_all_contours(numpy.zeros(heat_zone.shape, numpy.uint8), small_contours)
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
