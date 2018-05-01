from __future__ import annotations

from numbers import Real
from typing import Sequence, Tuple

from typecheck import typecheck
from vector import Vector, VectorType

RectType = Sequence[VectorType]


@typecheck(typecheck_setattr=True)
class Rect(RectType):
    def __len__(self) -> int:
        return 2

    def __getitem__(self, i: int) -> Vector:
        if i == 0:
            return self.pos1
        else:
            return self.pos2

    pos1: Vector
    pos2: Vector

    def __init__(self, pos1: VectorType, pos2: VectorType):
        x1, x2 = sorted((pos1[0], pos2[0]))
        y1, y2 = sorted((pos1[1], pos2[1]))
        self.pos1 = Vector(x1, y1)
        self.pos2 = Vector(x2, y2)

    def __repr__(self):
        return f"{self.__class__.__name__}{(self.pos1, self.pos2)}"

    def _sort_coordinates(self):
        if self.pos1.x > self.pos2.x:
            self.pos1.x, self.pos2.x = self.pos2.x, self.pos1.x
        if self.pos1.y > self.pos2.y:
            self.pos1.y, self.pos2.y = self.pos2.y, self.pos1.y

    @classmethod
    def from_xywh(cls, xy: VectorType, wh: VectorType):
        return Rect(Vector(xy), Vector(xy) + Vector(wh))

    def scale_wh(self, scale: VectorType) -> Rect:
        return Rect((self.pos1.x * scale[0], self.pos1.y * scale[1]), (self.pos2.x * scale[0], self.pos2.y * scale[1]))

    def collide_point(self, pos: VectorType) -> bool:
        return self.pos1.x <= pos[0] <= self.pos2[1] and self.pos1.y <= pos[1] <= self.pos2.y

    def collide_rect(self, other: Rect) -> bool:
        return any(self.collide_point(p) for p in (other.top_left, other.top_right, other.bottom_left, other.bottom_right)) or \
               any(other.collide_point(p) for p in (self.top_left, self.top_right, self.bottom_left, self.bottom_right))

    def relative_rect(self, parent: Rect) -> Rect:
        p1 = self.pos1 - parent.pos1
        p1 = Vector(p1.x / parent.w, p1.y / parent.h)
        p2 = self.pos2 - parent.pos1
        p2 = Vector(p2.x / parent.w, p2.y / parent.h)
        return self.__class__(p1, p2)

    def relative_point(self, point: VectorType) -> Vector:
        return (point - self.pos1) / self.wh

    @property
    def xywh(self) -> Tuple[Real, Real, Real, Real]:
        return self.left, self.top, self.width, self.height

    @property
    def width(self) -> Real:
        return self.pos2.x - self.pos1.x

    w = width

    @property
    def height(self) -> Real:
        return self.pos2.y - self.pos1.y

    h = height

    @property
    def size(self) -> Vector:
        return Vector(self.w, self.h)

    wh: Vector = size

    @property
    def left(self) -> Real:
        return self.pos1.x

    @left.setter
    def left(self, value: Real):
        self.pos1.x = value
        self._sort_coordinates()

    @property
    def right(self) -> Real:
        return self.pos2.x

    @right.setter
    def right(self, value: Real):
        self.pos2.x = value
        self._sort_coordinates()

    @property
    def top(self) -> Real:
        return self.pos1.y

    @top.setter
    def top(self, value: Real):
        self.pos1.y = value
        self._sort_coordinates()

    @property
    def bottom(self) -> Real:
        return self.pos2.y

    @bottom.setter
    def bottom(self, value: Real):
        self.pos2.y = value
        self._sort_coordinates()

    @property
    def top_left(self) -> Vector:
        return self.pos1

    @top_left.setter
    def top_left(self, value: Vector):
        self.pos1 = value
        self._sort_coordinates()

    xy: Vector = top_left

    @property
    def bottom_right(self) -> Vector:
        return self.pos2

    @bottom_right.setter
    def bottom_right(self, value: Vector):
        self.pos2 = value
        self._sort_coordinates()

    @property
    def top_right(self) -> Vector:
        return Vector(self.pos2.x, self.pos1.y)

    @top_right.setter
    def top_right(self, value: Vector):
        self.pos2.x, self.pos1.y = value
        self._sort_coordinates()

    @property
    def bottom_left(self) -> Vector:
        return Vector(self.pos1.x, self.pos2.y)

    @bottom_left.setter
    def bottom_left(self, value: VectorType):
        self.pos1.x, self.pos2.y = value
        self._sort_coordinates()

    @property
    def center(self) -> Vector:
        return Vector(self.pos1.x + self.w / 2, self.pos1.y + self.h / 2)
