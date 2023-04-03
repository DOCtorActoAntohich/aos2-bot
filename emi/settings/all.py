from emi.settings.game import GameSettings
from emi.settings.ocr import OcrSettings
from emi.settings.ui_800x600 import UiDescription800x600
from emi.settings.ui_1366x768 import UiDescription1366x768


class Settings:
    opencv_window_name = "Game view"
    game = GameSettings()
    ocr = OcrSettings()  # type: ignore # noqa: PGH003
    __ui_1366x168 = UiDescription1366x768()
    __ui_800x600 = UiDescription800x600()

    ui = __ui_1366x168
