from __future__ import annotations

import math
import random
from numbers import Real
from typing import Union, Sequence, cast, Tuple

from typecheck import typecheck

VectorType = Sequence[Real]


@typecheck(typecheck_setattr=True)
class Vector(VectorType):
    x: Real
    y: Real
    rotation: Real
    magnitude: Real
    __slots__ = ("x", "y")

    def __init__(self, x: Union[VectorType, Real], y: Real = None) -> None:
        if y is None:
            x, y = cast(VectorType, x)
        self.x, self.y = cast(Real, x), y

    def __repr__(self):
        return f"{type(self).__name__}{self.x, self.y}"

    def __len__(self) -> int:
        return 2

    def __getitem__(self, i: int) -> Real:
        return (self.x, self.y)[i]

    def __add__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't add Sequence with len {len(other)} to {type(self).__name__}")
        return Vector(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        if len(other) != 2:
            raise ValueError(f"Can't add Sequence with len {len(other)} to {type(self).__name__}")
        return Vector(other[0] + self.x, other[0] + self.y)

    def __iadd__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't add Sequence with len {len(other)} to {type(self).__name__}")
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't sub Sequence with len {len(other)} to {type(self).__name__}")
        return Vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't sub Sequence with len {len(other)} to {type(self).__name__}")
        return Vector(other[0] - self.x, other[1] - self.y)

    def __isub__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't sub Sequence with len {len(other)} to {type(self).__name__}")
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __mul__(self, other: Real) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: Real):
        return Vector(other * self.x, other * self.y)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __matmul__(self, other: VectorType):
        if len(other) != 2:
            raise ValueError(f"Can't mul Sequence with len {len(other)} and {type(self).__name__}")
        return Vector(self.x * other[0], self.y * other[1])

    def __rmatmul__(self, other):
        if len(other) != 2:
            raise ValueError(f"Can't mul Sequence with len {len(other)} and {type(self).__name__}")
        return Vector(other[0] * self.x, other[1] * self.y)

    def __imatmul__(self, other):
        if len(other) != 2:
            raise ValueError(f"Can't mul Sequence with len {len(other)} and {type(self).__name__}")
        self.x *= other[0]
        self.y *= other[1]
        return self

    def __truediv__(self, other: Union[VectorType, Real]) -> Vector:
        if isinstance(other, Sequence):
            if len(other) != 2:
                raise ValueError(f"Can't divide Sequence with len {len(other)} and {type(self).__name__}")
            return Vector(self.x / other[0], self.y / other[1])
        else:
            return Vector(self.x / other, self.y / other)

    def __rtruediv__(self, other: Union[VectorType, Real]) -> Vector:
        if isinstance(other, Sequence):
            if len(other) != 2:
                raise ValueError(f"Can't divide Sequence with len {len(other)} and {type(self).__name__}")
            return Vector(other[0] / self.x, other[1] / self.y)
        else:
            return Vector(other / self.x, other / self.y)

    def __itruediv__(self, other: Union[VectorType, Real]) -> Vector:
        if isinstance(other, Sequence):
            if len(other) != 2:
                raise ValueError(f"Can't divide Sequence with len {len(other)} and {type(self).__name__}")
            self.x /= other[0]
            self.y /= other[1]
            return self
        else:
            self.x /= other
            self.y /= other
            return self

    def __round__(self, n=None) -> Vector:
        return Vector(round(self.x, n), round(self.y, n))

    def change_rotation(self, rotation: Real) -> Vector:
        """Returns a new Vector with added rotation"""
        v = Vector(self.x, self.y)
        v.rotation += rotation
        return v

    def ser_rotation(self, rotation: Real) -> Vector:
        """Returns a new Vector with new rotation"""
        v = Vector(self.x, self.y)
        v.rotation = rotation
        return v

    def change_magnitude(self, magnitude: Real) -> Vector:
        """Returns a new Vector with added magnitude"""
        v = Vector(self.x, self.y)
        v.magnitude += magnitude
        return v

    def set_magnitude(self, magnitude: Real) -> Vector:
        """Returns a new Vector with new magnitude"""
        v = Vector(self.x, self.y)
        v.magnitude = magnitude
        return v

    @classmethod
    def random(cls, x_range=(0, 1), y_range=(0, 1)):
        """Creates a new Vector with random x and y values"""
        return cls(random.uniform(*x_range), random.uniform(*y_range))

    @classmethod
    def from_polar(cls, rotation: Real, magnitude: Real):
        """Creates a new Vector with the given rotation and magnitude"""
        return cls(math.cos(rotation) * magnitude, math.sin(rotation) * magnitude)

    def normalize(self):
        """Sets the magnitude to 1"""
        self.magnitude = 1

    @property
    def magnitude(self) -> Real:
        """The magnitude of the Vector"""
        return math.hypot(self.x, self.y)

    @magnitude.setter
    def magnitude(self, length: Real):
        f = length / self.magnitude
        self.x *= f
        self.y *= f

    @property
    def rotation(self) -> Real:
        """The rotation in radians of the Vector"""
        return math.atan2(self.x, self.y)

    @rotation.setter
    def rotation(self, angle: Real):
        m = self.magnitude
        self.x = math.sin(angle) * m
        self.y = math.cos(angle) * m

    @property
    def rounded(self) -> Tuple[Real, Real]:
        """A tuple with the x and y values of the Vector rounded to the nearest integer"""
        return round(self.x), round(self.y)
