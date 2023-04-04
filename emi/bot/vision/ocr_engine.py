import string

import numpy
import PIL.Image
import tesserocr

from emi.settings import Settings


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
        text_source = PIL.Image.fromarray(raw_image)
        engine.SetImage(text_source)
        return engine.GetUTF8Text().strip() or ""

    @classmethod
    def recognize_heat(cls, raw_image: numpy.ndarray) -> str:
        return cls.recognize_text(cls.for_heat_text(), raw_image)

    @classmethod
    def recognize_health(cls, raw_image: numpy.ndarray) -> str:
        return cls.recognize_text(cls.for_health_text(), raw_image)
