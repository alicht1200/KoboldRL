from __future__ import annotations

from typing import Iterator, Iterable, Tuple, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from source.entity import Actor
import source.map_generation.tile_types as tile_types

if TYPE_CHECKING:
    from source.engine import Engine
    from source.entity import Entity

class GameMap:
    def __init__(self, engine:Engine, width: int, height: int, tile : tile_types, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full(
            (width,height), fill_value= tile, order="F"
        )
        self.visible = np.full(
            (width,height), fill_value= False, order="F"
        )
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield  from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )


    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def in_bounds(self, x:int, y:int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console:Console) -> None:
        """
        Renders the map.

        if a tile is in 'visible' array, draw it in 'light' colors.
        if it isn't, but it's in 'explored'
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SEWER_SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda  x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, entity.color)

    @property
    def walkable_tiles(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y]["walkable"]:
                    yield x, y

    @property
    def swimmable_tiles(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y]["swimmable"]:
                    yield x, y

    @property
    def small_tiles(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y]["small"]:
                    yield x, y