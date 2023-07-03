from dataclasses import dataclass


@dataclass(init=True)
class Color:
    r: int
    g: int
    b: int

    @property
    def as_tuple(self) -> tuple[int, int, int]:
        return self.r, self.g, self.b
