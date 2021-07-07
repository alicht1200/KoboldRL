import numpy as np
from tcod.console import Console

import source.tile_types as tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width,height), fill_value=tile_types.wall, order="F")

        self.tiles[46:51, 1:54] = np.random.choice([tile_types.floor_clean, tile_types.floor_eroded, tile_types.floor_Rubble], (5, 53), p=[0.9, 0.06, 0.04])
        self.tiles[1:99, 45:50] = np.random.choice([tile_types.floor_clean, tile_types.floor_eroded, tile_types.floor_Rubble], (98, 5), p=[0.9, 0.06, 0.04])

        self.tiles[48, 0:55] = np.random.choice([tile_types.sludge1, tile_types.sludge2, tile_types.sludge3], 55, p=[0.5, 0.3, 0.2])
        self.tiles[48, 15] = tile_types.floor_bridge
        self.tiles[48, 40] = tile_types.floor_bridge

        self.tiles[0:100, 47] = np.random.choice([tile_types.sludge1, tile_types.sludge2, tile_types.sludge3], 100, p=[0.5, 0.3, 0.2])
        self.tiles[15, 47] = tile_types.floor_bridge
        self.tiles[40, 47] = tile_types.floor_bridge
        self.tiles[65, 47] = tile_types.floor_bridge
        self.tiles[80, 47] = tile_types.floor_bridge

    def in_bounds(self, x:int, y:int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console:Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]