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
        ("light", graphic_dt), # Graphics when tile is in FOV.
    ]
)

def new_tile(
        *, # Enfoce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        swimmable: int = 0,
        small: int = 0,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, swimmable, transparent, small, dark, light), dtype=tile_dt)

############################################
# SHROUD                                   #
############################################
"""
Used for unexplored map tiles. 
"""
SEWER_SHROUD =  np.array((ord(" "), (255, 255, 255), (5, 15, 10)), dtype=graphic_dt)
DUNGEON_SHROUD = np.array((ord(" "), (255, 255, 255), (5, 7, 15)), dtype=graphic_dt)
HOUSE_SHROUD = np.array((ord(" "), (255, 255, 255), (15, 10, 5)), dtype=graphic_dt)


############################################
# Colors                                   #
############################################

light_bridge_fg = (35, 30, 25)
light_bridge_bg = (55, 47, 37)
dark_bridge_fg = (15, 15, 10)
dark_bridge_bg = (45, 37, 20)

light_sewer_floor_fg = (20, 25, 20)
light_sewer_floor_bg = (27, 30, 26)
dark_sewer_floor_fg = (10, 15, 5)
dark_sewer_floor_bg = (15, 20, 10)

light_sluge_fg = (85, 120, 50)
light_sluge_bg = (102, 135, 50)
dark_sluge_fg = (40, 46, 20)
dark_sluge_bg = (32, 40, 15)

light_sewer_wall_fg = (50, 55, 55)
light_sewer_wall_bg = (15, 20, 15)
dark_sewer_wall_fg = (20, 25, 20)
dark_sewer_wall_bg = (15, 20, 15)


############################################
# Tile Data Base                           #
############################################

"""Sewer tiles"""
floor_bridge = new_tile(
    walkable=True,
    swimmable=True,
    transparent=True,
    dark=(ord("≡"), dark_bridge_fg, dark_bridge_bg),
    light=(ord("≡"), light_bridge_fg, light_bridge_bg),
)
sludge1 = new_tile(
    walkable=False,
    swimmable=True,
    transparent=True,
    dark=(ord(" "), dark_sluge_fg, dark_sluge_bg),
    light=(ord(" "), light_sluge_fg, light_sluge_bg),
)
sludge2 = new_tile(
    walkable=False,
    swimmable=True,
    transparent=True,
    dark=(ord("~"), dark_sluge_fg, dark_sluge_bg),
    light=(ord("~"), light_sluge_fg, light_sluge_bg),
)
sludge3 = new_tile(
    walkable=False,
    swimmable=True,
    transparent=True,
    dark=(ord("≈"), dark_sluge_fg, dark_sluge_bg),
    light=(ord("≈"), light_sluge_fg, light_sluge_bg),
)
sewer_floor_clean = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("┼"), dark_sewer_floor_fg, dark_sewer_floor_bg),
    light=(ord("┼"), light_sewer_floor_fg, light_sewer_floor_bg),
)
sewer_floor_eroded = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), dark_sewer_floor_fg, dark_sewer_floor_bg),
    light=(ord(" "), light_sewer_floor_fg, light_sewer_floor_bg),
)
sewer_floor_Rubble = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("•"), dark_sewer_floor_fg, dark_sewer_floor_bg),
    light=(ord("•"), light_sewer_floor_fg, light_sewer_floor_bg),
)
sewer_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("▓"), dark_sewer_wall_fg, dark_sewer_wall_bg),
    light=(ord("▓"), light_sewer_wall_fg, light_sewer_wall_bg),
)

"""Dungeon tiles"""

dungeon_floor_clean = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("┼"), (35, 30, 40), (37, 37, 43)),
    light=(ord("┼"), (35, 30, 40), (37, 37, 43)),
)
dungeon_floor_eroded = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "),  (35, 30, 40), (37, 37, 43)),
    light=(ord(" "),  (35, 30, 40), (37, 37, 43)),
)
dungeon_floor_Rubble = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(";"),  (35, 30, 40), (37, 37, 43)),
    light=(ord(";"), (35, 30, 40), (37, 37, 43)),
)
dungeon_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("▓"), (38, 40, 50), (35, 40, 41)),
    light=(ord("▓"), (38, 40, 50), (35, 40, 41)),
)

"""" Small passages """
small_corridor = new_tile(
    walkable=True,
    small=True,
    transparent=False,
    dark=(ord("·"), (50, 40, 10), (20, 20, 15)),
    light=(ord("·"), (50, 40, 10), (20, 20, 15)),
)