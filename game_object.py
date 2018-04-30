from __future__ import annotations

from typing import List, ClassVar, Tuple, Type, TypeVar, Optional


class NotFoundError(ValueError):
    pass


class GameObjectNotFound(NotFoundError):
    pass


class ComponentNotFound(NotFoundError):
    pass


class GameObject:
    _game_objects: ClassVar[List[GameObject]]
    name: str
    tag: str = None
    components: List[Component]
    children: List[GameObject]

    def __init__(self, name=None):
        if name is None:
            name = "GameObject" + str(len(self._game_objects))
        self.name = name
        self.components = []

    def add_component(self, component_class: Type[T]) -> T:
        self.components.append(component_class(self))
        return self.components[-1]

    def get_components(self, component_class: Type[T]) -> List[T]:
        return [c for c in self.components if isinstance(c, component_class)]

    def get_component(self, component_class: Type[T]) -> T:
        r = self.get_components(component_class)
        if not r:
            raise ComponentNotFound(component_class)
        return r[0]

    @property
    def renderers(self) -> Tuple[Renderer, ...]:
        return tuple(c for c in self.components if isinstance(c, Renderer))

    @property
    def renderer(self) -> Renderer:
        return self.get_component(Renderer)

    @property
    def transform(self) -> Optional[Transform]:
        try:
            return self.get_component(Transform)
        except ComponentNotFound:
            return

    @classmethod
    def find_by_name(cls, name: str):
        for go in cls._game_objects:
            if go.name == name:
                return go
        else:
            raise GameObjectNotFound(f"Can't find any GameObject with name {name}")

    @classmethod
    def find_by_tag(cls, tag: str):
        for go in cls._game_objects:
            if go.tag == tag:
                return go
        else:
            raise GameObjectNotFound(f"Can't find any GameObject with tag {tag}")


from components import Renderer, Transform, Component

T = TypeVar("T", bound=Component)
