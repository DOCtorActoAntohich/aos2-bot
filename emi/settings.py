from pydantic import BaseSettings, Field
import win32con


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


class Settings:
    game_name = "Acceleration of SUGURI 2"
    opencv_window_name = "Game view"
    control_keys = _GameKeys()
