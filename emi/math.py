class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def as_tuple(self):
        return self.x, self.y


class Rect:
    @classmethod
    def from_tuple(cls, rect: tuple[int, int, int, int]):
        left, top, right, bottom = rect
        return cls(left, top, right, bottom)

    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def x(self):
        return self.left

    @property
    def y(self):
        return self.top

    @property
    def as_tuple(self):
        return self.left, self.top, self.right, self.bottom
