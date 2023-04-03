from __future__ import annotations

import enum

from emi.settings import Settings


class Controls(enum.Enum):
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()
    Dash = enum.auto()

    @classmethod
    def convert_to_key_code(cls, control: Controls) -> str:
        # TODO add remaining buttons
        mapping = {
            Controls.Up: Settings.game.control_keys.Up,
            Controls.Down: Settings.game.control_keys.Down,
            Controls.Left: Settings.game.control_keys.Left,
            Controls.Right: Settings.game.control_keys.Right,
            Controls.Dash: Settings.game.control_keys.Dash,
        }
        return mapping[control]

    def to_key_code(self) -> str:
        return Controls.convert_to_key_code(self)
