from typing import Tuple

import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
[
    ("ch", np.int32), # Unicode codepoint.for
    ("fg", "3B"), # 3 unsigned bytes, for RGB colors.
    ("bg", "3B"), # 3 unsigned bytes, for RGB colors.
]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_), # True if this tile can be walked over.
        ("swimmable", np.bool_), # True if this tile can be swimmed through.
        ("transparent", np.bool_), # True if this tile dosen't block FOV.
        ("small", np.bool_), # True if this tile only allow passage for small creatures
        ("dark", graphic_dt), # Graphics when tile is out of FOV.
    ]
)

def new_tile(
        *, # Enfoce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        swimmable: int = 0,
        small: int = 0,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, swimmable, transparent, small, dark), dtype=tile_dt)

############################################
# Tile Data Base                           #
############################################

"""Sewer tiles"""
floor_bridge = new_tile(
    walkable=True, transparent=True, dark=(ord("≡"), (35, 30, 25), (55, 47, 37)),
)
sludge1 = new_tile(
    walkable=False, swimmable=True, transparent=True, dark=(ord(" "), (44, 66, 44), (32, 40, 15)),
)
sludge2 = new_tile(
    walkable=False, swimmable=True, transparent=True, dark=(ord("~"), (25, 35, 7), (32, 40, 15)),
)
sludge3 = new_tile(
    walkable=False, swimmable=True, transparent=True, dark=(ord("≈"), (25, 35, 7), (32, 40, 15)),
)
sewer_floor_clean = new_tile(
    walkable=True, transparent=True, dark=(ord("┼"), (10, 15, 5), (15, 20, 10)),
)
sewer_floor_eroded = new_tile(
    walkable=True, transparent=True, dark=(ord(" "),  (10, 15, 5), (15, 20, 10)),
)
sewer_floor_Rubble = new_tile(
    walkable=True, transparent=True, dark=(ord("•"),  (10, 15, 5), (15, 20, 10)),
)
sewer_wall = new_tile(
    walkable=False, transparent=False, dark=(ord("▓"), (20, 25, 20), (15, 20, 15)),
)

"""Dungeon tiles"""

dungeon_floor_clean = new_tile(
    walkable=True, transparent=True, dark=(ord("┼"), (35, 30, 40), (37, 37, 43)),
)
dungeon_floor_eroded = new_tile(
    walkable=True, transparent=True, dark=(ord(" "),  (35, 30, 40), (37, 37, 43)),
)
dungeon_floor_Rubble = new_tile(
    walkable=True, transparent=True, dark=(ord(";"),  (35, 30, 40), (37, 37, 43)),
)
dungeon_wall = new_tile(
    walkable=False, transparent=False, dark=(ord("▓"), (38, 40, 50), (35, 40, 41)),
)

"""" Small passages """
small_corridor = new_tile(
    walkable=True, small=True, transparent=True, dark=(ord("·"), (50, 40, 10), (20, 20, 15)),
)