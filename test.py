from __future__ import annotations

import pygame
from pygame_application import Scene, Application

from color import Color
from components import Transform, SolidColorRenderer
from game_object import GameObject
from game_scene import GameScene
from rect import Rect
from vector import Vector


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


test_obj = GameObject("TestObj")
transform = test_obj.add_component(Transform)
transform.pos = Vector(4, 4)
renderer = test_obj.add_component(SolidColorRenderer)
renderer.offset.x = 1
renderer.color = Color(1, 1, 0)
game_scene = GameScene("Test", [test_obj], Color(1., 1., 1.))
app = Application((640, 640), "", resizable=True)
app.run(DisplayScene(game_scene))
