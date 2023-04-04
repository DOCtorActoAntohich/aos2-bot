from dataclasses import dataclass


@dataclass(init=True)
class Color:
    r: int
    g: int
    b: int
