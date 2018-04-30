from __future__ import annotations

import math
import random
from numbers import Real
from typing import Union, Sequence, cast

from typecheck import typecheck

VectorType = Sequence[Real]


@typecheck(typecheck_setattr=True)
class Vector(VectorType):
    x: Real
    y: Real
    rotation: Real
    magnitude: Real

    def __init__(self, x: Union[VectorType, Real], y: Real = None) -> None:
        if y is None:
            x, y = cast(VectorType, x)
        self.x, self.y = cast(Real, x), y

    def __repr__(self):
        return f"{self.__class__.__name__}{self.x, self.y}"

    def __len__(self) -> int:
        return 2

    def __getitem__(self, i: int) -> Real:
        return (self.x, self.y)[i]

    def __add__(self, other: VectorType):
        return Vector(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __iadd__(self, other: VectorType):
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other: VectorType):
        return Vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: VectorType):
        return Vector(other[0] - self.x, other[1] - self.y)

    def __isub__(self, other: VectorType):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __mul__(self, other: Real) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: Real):
        return Vector(self.x * other, self.y * other)

    def __matmul__(self, other: VectorType):
        return Vector(self.x * other[0], self.y * other[1])

    def __rmatmul__(self, other):
        return Vector(other[0] * self.x, other[1] * self.y)

    def __truediv__(self, other: Union[VectorType, Real]) -> Vector:
        if isinstance(other, Sequence):
            return Vector(self.x / other[0], self.y / other[1])
        return Vector(self.x / other, self.y / other)

    def __rtruediv__(self, other: VectorType) -> Vector:
        self.x /= other
        self.y /= other
        return self

    def __round__(self, n=None) -> Vector:
        return Vector(round(self.x, n), round(self.y, n))

    def change_rotation(self, rotation: float) -> Vector:
        v = Vector(self.x, self.y)
        v.rotation += rotation
        return v

    @classmethod
    def random(cls, x_range=(0, 1), y_range=(0, 1)):
        return cls(random.uniform(*x_range), random.uniform(*y_range))

    @classmethod
    def from_polar(cls, rotation: Real, magnitude: Real):
        return Vector(math.cos(rotation) * magnitude, math.sin(rotation) * magnitude)

    def normalize(self):
        f = self.magnitude
        self.x *= f
        self.y *= f
        return self

    @property
    def magnitude(self) -> Real:
        return (self.x * self.x + self.y * self.y) ** 0.5

    @magnitude.setter
    def magnitude(self, value: Real):
        f = value / self.magnitude
        self.x *= f
        self.y *= f

    @property
    def rotation(self):
        return math.atan2(self.x, self.y)

    @rotation.setter
    def rotation(self, value):
        m = self.magnitude
        self.x = math.sin(value)
        self.y = math.cos(value)
        self.magnitude = m

    @property
    def rounded(self):
        return round(self.x), round(self.y)
