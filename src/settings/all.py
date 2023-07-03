from src.settings.game import GameSettings
from src.settings.ocr import OcrSettings
from src.settings.ui_800x600 import UiDescription800x600
from src.settings.ui_1366x768 import UiDescription1366x768
from src.settings.yolo import YoloSettings


class Settings:
    opencv_window_name = "Game view"
    game = GameSettings()
    ocr = OcrSettings()  # type: ignore # noqa: PGH003
    yolo = YoloSettings()
    __ui_1366x168 = UiDescription1366x768()
    __ui_800x600 = UiDescription800x600()

    ui = __ui_1366x168
