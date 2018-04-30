from __future__ import annotations

import math
from typing import Hashable, Dict, Tuple, Any

import pygame

from color import Color
from rect import Rect
from resource_loader import load_image
from vector import Vector


class Component:
    game_object: GameObject

    def __init__(self, game_object: GameObject):
        self.game_object = game_object


class Transform(Component):
    pos: Vector
    scale: Vector
    rotation: float

    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.pos = Vector(0, 0)
        self.scale = Vector(1, 1)
        self.rotation = 0


class Renderer(Component):
    image: pygame.Surface
    rect: Rect


class CachedRenderer(Renderer):
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self._cache: Dict[Hashable, Tuple[pygame.Surface, Rect]] = {}

    def _get_args(self) -> Hashable:
        raise NotImplementedError

    def _render(self, args: Hashable) -> pygame.Surface:
        raise NotImplementedError

    def _render_rect(self, args: Hashable, img: pygame.Surface) -> Rect:
        raise NotImplementedError

    def _set_image(self, value: Any) -> bool:
        pass

    @property
    def image(self):
        args = self._get_args()
        if args not in self._cache:
            img = self._render(args)
            rect = self._render_rect(args, img)
        else:
            img, _ = self._cache[args]
        return img

    @image.setter
    def image(self, value: Any):
        r = self._set_image(value)
        if not r:
            raise TypeError(f"Can't set 'image' attribute of class '{self.__class__.__name__}'")
        self._cache = {}

    @property
    def rect(self):
        args = self._get_args()
        if args not in self._cache:
            img = self._render(args)
            rect = self._render_rect(args, img)
            self._cache[args] = img, rect
        else:
            _, rect = self._cache[args]
        return rect


class TransformedImageRenderer(CachedRenderer):
    _image: pygame.Surface
    offset: Vector

    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self._image = load_image("")
        self.offset = Vector(0, 0)

    def _get_args(self) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
        transform: Transform = self.game_object.transform
        return tuple(round(transform.pos, 2)), tuple(round(transform.scale, 2)), round(transform.rotation, 2)

    def _render(self, args: Hashable):
        pos, scale, rotation = args
        return pygame.transform.rotate(pygame.transform.scale(self._image, Vector(scale) @ self._image.get_size()), rotation)

    def _render_rect(self, args: Hashable, img: pygame.Surface):
        pos, scale, rotation = args
        scale = Vector(scale)
        wh: Vector = scale / self._image.get_size() @ img.get_size()
        r = Rect.from_xywh(pos - (wh / 2) + self.offset.change_rotation(math.radians(rotation)), wh)
        return r

    def _set_image(self, value: pygame.Surface):
        self._image = value
        return True


class SolidColorRenderer(TransformedImageRenderer):
    _color: Color

    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self._color = None

    @property
    def resolution(self) -> Tuple[int, int]:
        return self._image.get_size()

    @resolution.setter
    def resolution(self, value: Tuple[int, int]):
        self._image = pygame.transform.scale(self._image, value)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self._image.fill(value.rgb_255)


class Collider(Component):
    def collide_with(self, other: Collider) -> bool:
        raise NotImplementedError


class RectCollider(Collider):
    rect: Rect

    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        self.rect = None

    def collide_with(self, other: Collider) -> bool:
        if self.rect is None:
            return False
        if isinstance(other, RectCollider):
            return self.rect.collide_rect(other.rect)
        return NotImplemented


from game_object import GameObject
