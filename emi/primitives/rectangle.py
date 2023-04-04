from __future__ import annotations


class Rectangle:
    @classmethod
    def from_tuple(cls, rect: tuple[int, int, int, int]) -> Rectangle:
        left, top, right, bottom = rect
        return cls(left, top, right, bottom)

    def __init__(self, left: int, top: int, right: int = 0, bottom: int = 0) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def at_position(self, x: int, y: int) -> Rectangle:
        return Rectangle(x, y, x + self.width, y + self.height)

    def with_size(self, width: int, height: int) -> Rectangle:
        return Rectangle(self.x, self.y, self.x + width, self.y + height)

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def x(self) -> int:
        return self.left

    @property
    def y(self) -> int:
        return self.top

    @property
    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.left, self.top, self.right, self.bottom
