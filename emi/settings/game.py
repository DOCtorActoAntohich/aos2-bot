from pydantic import BaseSettings, Field

from emi.primitives import Color


class _GameKeysSettings(BaseSettings):
    Up: str = Field("up", env="GAME_BUTTON_UP")
    Down: str = Field("down", env="GAME_BUTTON_DOWN")
    Left: str = Field("left", env="GAME_BUTTON_LEFT")
    Right: str = Field("right", env="GAME_BUTTON_RIGHT")
    Dash: str = Field("space", env="GAME_BUTTON_DASH")

    # TODO add remaining buttons baka

    class Config:
        env_file = ".env"


class GameSettings:
    name = "Acceleration of SUGURI 2"
    control_keys = _GameKeysSettings()  # type: ignore # noqa: PGH003
    p1_attack_indicator_color = Color(0, 0, 255)
    p2_attack_indicator_color = Color(255, 0, 0)
    MinHeat = 0
    MaxHeat = 300
    MinHealth = 0
    MaxHealth = 9000
