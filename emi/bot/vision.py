from __future__ import annotations

import string

import cv2
import numpy
import tesserocr
from PIL import Image

from emi.math import Rect
from emi.settings import Settings


def crop_rect(image: numpy.ndarray, rect: Rect) -> numpy.ndarray:
    return image[rect.top:rect.bottom, rect.left:rect.right]


class OcrError(Exception):
    pass


class OcrEngine:
    __heat_text_engine: tesserocr.PyTessBaseAPI = None

    @classmethod
    def for_heat_text(cls) -> tesserocr.PyTessBaseAPI:
        if cls.__heat_text_engine is None:
            cls.__heat_text_engine = tesserocr.PyTessBaseAPI(path=Settings.ocr.data_path)
            cls.__heat_text_engine.SetPageSegMode(tesserocr.PSM.SINGLE_LINE)
            cls.__heat_text_engine.SetVariable("tessedit_char_whitelist", string.digits)
            cls.__heat_text_engine.Init(lang="eng", oem=tesserocr.OEM.LSTM_ONLY, path=Settings.ocr.data_path)
        return cls.__heat_text_engine


class HeatTextContour:
    MinArea = 10
    MaxArea = 3000
    MinAspectRatio = 0.2
    MaxAspectRatio = 1.0

    @classmethod
    def has_suitable_area(cls, area: float) -> bool:
        return cls.MinArea <= area <= cls.MaxArea

    @classmethod
    def has_suitable_aspect_ratio(cls, aspect_ratio):
        return cls.MinAspectRatio <= aspect_ratio <= cls.MaxAspectRatio


class InterfaceData:
    RedHeatTextGrayscaleThreshold = 105
    LettersLikeNumbers = {
        "o": "0",
        "s": "5",
    }

    def __init__(self, grayscale_frame: numpy.ndarray) -> None:
        self.ui_frame = crop_rect(grayscale_frame, Settings.ui.Position)

    @property
    def p1_heat(self) -> int:
        heat_zone = crop_rect(self.ui_frame, Settings.ui.p1.HeatPosition)
        text = self.__recognize_heat(self.ui_frame)
        return self.__corrected_heat(text)

    def __recognize_heat(self, ui_crop: numpy.ndarray) -> str:
        _, binary_image = cv2.threshold(ui_crop, self.RedHeatTextGrayscaleThreshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        small_contours = self.__filter_heat_text_contours(contours)

        mask = numpy.zeros(ui_crop.shape, numpy.uint8)
        cv2.drawContours(mask, small_contours, -1, 255, -1)
        masked_ui_crop = cv2.bitwise_and(ui_crop, ui_crop, mask=mask)

        p1_heat_zone = crop_rect(masked_ui_crop, Settings.ui.p1.HeatPosition)
        p1_heat_zone = cv2.add(p1_heat_zone, 50)
        p1_heat_zone = cv2.fastNlMeansDenoising(p1_heat_zone, None, 10, 7, 21)

        image = Image.fromarray(p1_heat_zone)

        OcrEngine.for_heat_text().SetImage(image)
        return OcrEngine.for_heat_text().GetUTF8Text().strip() or ""

    @classmethod
    def __filter_heat_text_contours(cls, contours) -> list:
        suitable_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, width, height = cv2.boundingRect(contour)
            aspect_ratio = width / height
            if HeatTextContour.has_suitable_area(area) and HeatTextContour.has_suitable_aspect_ratio(aspect_ratio):
                suitable_contours.append(contour)
        return suitable_contours

    def __corrected_heat(self, heat_text: str) -> int:
        fixed_text = ""
        for character in heat_text.lower():
            if character.isdigit():
                fixed_text += character
            if character in self.LettersLikeNumbers:
                fixed_text += self.LettersLikeNumbers[character]

        if len(fixed_text) == 0:
            raise OcrError

        heat = int(fixed_text)
        if not Settings.game.MinHeat <= heat <= Settings.game.MaxHeat:
            raise OcrError

        return heat
