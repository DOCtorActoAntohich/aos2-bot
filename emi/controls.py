from __future__ import annotations

import enum

from emi.settings import Settings


class Controls(enum.Enum):
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()
    Dash = enum.auto()

    # TODO uncomment after initial testing
    # WeaponA = enum.auto()
    # WeaponB = enum.auto()
    # Special = enum.auto()
    # Hyper = enum.auto()
    # Shield = enum.auto()

    @classmethod
    def convert_to_key_code(cls, control: Controls) -> str:
        mapping = {
            Controls.Up: Settings.game.control_keys.Up,
            Controls.Down: Settings.game.control_keys.Down,
            Controls.Left: Settings.game.control_keys.Left,
            Controls.Right: Settings.game.control_keys.Right,
            Controls.Dash: Settings.game.control_keys.Dash,
            # TODO uncomment after initial testing
            # Controls.WeaponA: Settings.game.control_keys.WeaponA,
            # Controls.WeaponB: Settings.game.control_keys.WeaponB,
            # Controls.Special: Settings.game.control_keys.Special,
            # Controls.Shield: Settings.game.control_keys.Shield,
            # Controls.Hyper: Settings.game.control_keys.Hyper
        }
        return mapping[control]

    def to_key_code(self) -> str:
        return Controls.convert_to_key_code(self)
