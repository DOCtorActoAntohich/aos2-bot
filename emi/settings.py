import os
import pathlib

from pydantic import BaseSettings, Field

from emi.math import Rect

DOTENV_PATH = pathlib.Path(os.getcwd()) / ".env"


class _GameKeys(BaseSettings):
    Up: str = Field("up", env="GAME_BUTTON_UP")
    Down: str = Field("down", env="GAME_BUTTON_DOWN")
    Left: str = Field("left", env="GAME_BUTTON_LEFT")
    Right: str = Field("right", env="GAME_BUTTON_RIGHT")
    Dash: str = Field("space", env="GAME_BUTTON_DASH")

    # TODO uncomment after initial testing
    # WeaponA: str = Field("z", env="GAME_BUTTON_WEAPON_A")
    # WeaponB: str = Field("x", env="GAME_BUTTON_WEAPON_B")
    # Special: str = Field("c", env="GAME_BUTTON_WEAPON_SPECIAL")
    # Shield: str = Field("v", env="GAME_BUTTON_SHIELD")
    # Hyper: str = Field("shift", env="GAME_BUTTON_HYPER")

    class Config:
        env_file = DOTENV_PATH


class _Ocr(BaseSettings):
    data_path: str = Field(..., env="TESSDATA_PREFIX")

    class Config:
        env_file = DOTENV_PATH


class _Player1UI:
    HealthPosition = Rect(92, 36).with_size(220, 20)
    MeterBarsPosition = Rect(170, 64).with_size(130, 40)
    HeatPosition = Rect(358, 67).with_size(60, 34)
    DashCancelIconPosition = Rect(576, 90).with_size(60, 25)


class _Player2UI:
    HealthPosition = Rect(1058, 36).with_size(220, 20)
    MeterBarsPosition = Rect(1070, 64).with_size(130, 40)
    HeatPosition = Rect(972, 69).with_size(90, 30)
    DashCancelIconPosition = Rect(728, 90).with_size(60, 25)


class _UI:
    p1 = _Player1UI()
    p2 = _Player2UI()
    Position = Rect(0, 0).with_size(1366, 140)
    TimerPosition = Rect(618, 0).with_size(128, 80)


class _Game:
    name = "Acceleration of SUGURI 2"
    control_keys = _GameKeys()
    MinHeat = 0
    MaxHeat = 300
    MinHealth = 0
    MaxHealth = 9000


class Settings:
    game = _Game()
    opencv_window_name = "Game view"
    ocr = _Ocr()
    ui = _UI()
