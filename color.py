from __future__ import annotations

from typing import Sequence, Union, cast

ColorType = Sequence[float]


class Color(ColorType):
    def __init__(self, r: Union[ColorType, float], g: float = None, b: float = None) -> None:
        if g is b is None:
            if isinstance(r, Sequence):
                r, g, b = r
            else:
                g = b = r
        if not all(isinstance(v, (float, int)) for v in (r, g, b)):
            raise TypeError((r, g, b))
        self.r: float = cast(float,r)
        self.g: float = g
        self.b: float = b

    def __repr__(self):
        return f"{self.__class__.__name__}{(self.r, self.g, self.b)}"

    @property
    def rgb_255(self):
        return tuple(int(v * 255) for v in (self.r, self.g, self.b))

    def __len__(self):
        return 3

    def __getitem__(self, item):
        return (self.r, self.g, self.b)[item]
