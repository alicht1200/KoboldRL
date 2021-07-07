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
        ("transparent", np.bool_), # True if this tile dosen't block FOV.
        ("small", np.bool_), # True if this tile only allow passage for small creatures
        ("dark", graphic_dt), # Graphics when tile is out of FOV.
    ]
)

def new_tile(
        *, # Enfoce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        small: int = 0,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, small, dark), dtype=tile_dt)

############################################
# Tile Data Base                           #
############################################

floor_clean = new_tile(
    walkable=True, transparent=True, small= False, dark=(ord("┼"), (30, 35, 25), (37, 43, 27)),
)
floor_bridge = new_tile(
    walkable=True, transparent=True, small= False, dark=(ord("≡"), (35, 30, 25), (55, 47, 37)),
)

sludge1 = new_tile(
    walkable=False, transparent=True, small= False, dark=(ord(" "), (44, 66, 44), (28, 48, 0)),
)

sludge2 = new_tile(
    walkable=False, transparent=True, small= False, dark=(ord("~"), (25, 43, 7), (28, 48, 0)),
)

sludge3 = new_tile(
    walkable=False, transparent=True, small= False, dark=(ord("≈"), (25, 43, 7), (28, 48, 0)),
)

floor_eroded = new_tile(
    walkable=True, transparent=True, small= False, dark=(ord(" "),  (30, 35, 25), (37, 43, 27)),
)
floor_Rubble = new_tile(
    walkable=True, transparent=True, small= False, dark=(ord("•"),  (34, 37, 25), (37, 43, 27)),
)
wall = new_tile(
    walkable=False, transparent=False, small= False, dark=(ord("▓"), (61, 60, 47), (41, 40, 35)),
)