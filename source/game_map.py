import numpy as np
from tcod.console import Console
from typing import Iterator, List, Tuple, TYPE_CHECKING

import source.tile_types as tile_types

class GameMap:
    def __init__(self, width: int, height: int, tile : tile_types):
        self.width, self.height = width, height
        self.tiles = np.full((width,height), fill_value= tile, order="F")


    def in_bounds(self, x:int, y:int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console:Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

    @property
    def walkable_tiles(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y]["walkable"]:
                    yield x, y
