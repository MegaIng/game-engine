from __future__ import annotations

import math
from typing import List, Iterable

import pygame
from pygame_application import Scene

from color import Color
from color import ColorType
from game_object import GameObject
from rect import Rect
from typecheck import typecheck
from vector import Vector

Rect0011 = Rect((0, 0), (1, 1))

@typecheck(typecheck_setattr=True)
class GameScene:
    name: str
    game_objects: List[GameObject]
    background: Color

    def __init__(self, name: str, game_objects: Iterable[GameObject], background: ColorType):
        self.name = name
        self.game_objects = list(game_objects)
        self.background = Color(background)

    def render(self, screen: pygame.Surface, screen_rect: Rect, *, debug=False):
        screen.fill(self.background.rgb_255)
        for obj in self.game_objects:
            for renderer in obj.renderers:
                if renderer.image is not None and renderer.rect is not None:
                    rel = renderer.rect.relative_rect(screen_rect)
                    if not rel.collide_rect(Rect0011):
                        if debug:
                            print(f"Did not render '{renderer}' of object '{obj}' (Not on screen)")
                        continue
                    rect_on_screen = rel.scale_wh(screen.get_size())
                    img = pygame.transform.scale(renderer.image, rect_on_screen.wh.rounded)
                    screen.blit(img, rect_on_screen.xy.rounded)
                else:
                    if debug:
                        print(f"Did not render '{renderer}' of object '{obj}' (No Image or Rect)")
            if debug and not obj.renderers:
                print(f"Did not render  object '{obj}' (No Renderer)")
            if obj.transform and debug:
                t = obj.transform
                p1 = (screen_rect.relative_point(t.pos) @ screen.get_size()).rounded
                p2 = (screen_rect.relative_point(t.pos + Vector.from_polar(math.radians(-t.rotation), 1)) @ screen.get_size()).rounded
                pygame.draw.circle(screen, (255, 0, 0), p1, 5)
                pygame.draw.line(screen, (0, 255, 0), p1, p2, 3)
            elif debug:
                print(f"Did not debug object '{obj}' (No Transform)")


class DisplayScene(Scene):
    def __init__(self, game_scene: GameScene):
        self.game_scene = game_scene
        self.screen_rect = Rect((0, 0), (10, 10))

    def on_enter(self, previous_scene: 'Scene' = None, multi_id: int = None):
        pygame.display.set_caption(self.game_scene.name)

    def draw(self, screen: pygame.Surface, multi_id: int = None):
        self.game_scene.render(screen, self.screen_rect, debug=True)

    def update(self, dt: int, multi_id: int = None):
        self.game_scene.game_objects[0].transform.rotation += dt / 100
