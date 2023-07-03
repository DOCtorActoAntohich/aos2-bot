from __future__ import annotations

from typing import Generic, TypeVar

Number = TypeVar("Number", int, float)


class Rectangle(Generic[Number]):
    @classmethod
    def from_tuple(cls, rect: tuple[Number, Number, Number, Number]) -> Rectangle:
        left, top, right, bottom = rect
        return cls(left, top, right, bottom)

    def __init__(self, left: Number, top: Number, right: Number = 0, bottom: Number = 0) -> None:
        self.left: Number = left
        self.top: Number = top
        self.right: Number = right
        self.bottom: Number = bottom

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        coordinates = ", ".join(str(i) for i in self.as_tuple)
        return f"{self.__class__.__name__}({coordinates})"

    def at_position(self, x: Number, y: Number) -> Rectangle:
        return Rectangle(x, y, x + self.width, y + self.height)

    def with_size(self, width: Number, height: Number) -> Rectangle:
        return Rectangle(self.x, self.y, self.x + width, self.y + height)

    @property
    def width(self) -> Number:
        return self.right - self.left

    @property
    def height(self) -> Number:
        return self.bottom - self.top

    @property
    def x(self) -> Number:
        return self.left

    @property
    def y(self) -> Number:
        return self.top

    @property
    def as_tuple(self) -> tuple[Number, Number, Number, Number]:
        return self.left, self.top, self.right, self.bottom
