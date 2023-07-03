from __future__ import annotations


class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y
