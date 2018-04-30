from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pygame


def get_path(name: str, suffixes: Tuple[str, ...], default: str):
    if not name:
        return default
    path = Path(name)
    if path.exists():
        return str(path)
    for s in suffixes:
        p = path.with_suffix(s)
        if p.exists():
            return str(p)
    else:
        return default


_image_cache = {}


def _load_image_cached(path: str):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path)
    return _image_cache[path]


def load_image(name: str, min_resolution=(1000, 1000)) -> pygame.Surface:
    target_path = get_path(name, ("png",), "missing.png")
    img: pygame.Surface = _load_image_cached(target_path).copy()
    if img.get_width() < min_resolution[0]:
        f = min_resolution[0] / img.get_width()
        img = pygame.transform.scale(img, (min_resolution[0], int(img.get_height() * f)))
    if img.get_height() < min_resolution[1]:
        f = min_resolution[1] / img.get_height()
        img = pygame.transform.scale(img, (int(img.get_width() * f), min_resolution[1]))
    return img
