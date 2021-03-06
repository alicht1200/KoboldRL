from __future__ import annotations

import random
from typing import Iterator, List, Tuple

import source.map_generation.tile_types as tile_types
import tcod
from numpy.random import choice as np_choice
from numpy.random import seed as np_seed

from source.engine import Engine
from source.game_map import GameMap
from source.map_generation.rooms import RectangularRoom
import source.map_generation.monster_tables as monster_tables

MAX_MONSTERS_PER_ROOM = 4

def tunnel_corridor(
        start: Tuple[int, int], end: Tuple[int, int]
)-> Iterator[Tuple[int, int]]:
    """Return an L-Shaped corridor between two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        #Horizontal first, vertical later.
        corner_x, corner_y = x2, y1
    else:
        # Vertical first, horizontal later.
        corner_x, corner_y = x1, y2

    #digs the corridor
    for x,y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def tunnel_sewer(dungeon, direction, x_focus, y_focus) -> Tuple[RectangularRoom, str]:
    tunnel_width = np_choice([4, 6], p=[0.25, 0.75])
    if direction == 'h':
        tunnel_length = random.randint(20, dungeon.width - 1)
        x = random.randint(max(0, (x_focus - tunnel_length)), min(dungeon.width - tunnel_length - 1, x_focus))
        y = min(max(tunnel_width, y_focus), (dungeon.height - tunnel_width - 1))
        tunnel = RectangularRoom(x, y, tunnel_length, tunnel_width)
        return tunnel, 'h'
    else:
        tunnel_length = random.randint(20, dungeon.height - 1)
        x = min(max(tunnel_width, x_focus), (dungeon.width - tunnel_width - 1))
        y = random.randint(max(0, (y_focus - tunnel_length)), min(dungeon.height - tunnel_length - 1, y_focus))
        tunnel = RectangularRoom(x, y, tunnel_width, tunnel_length)
        return tunnel, 'v'

def populate_sewer_water(dungeon: GameMap, max_monsters: int) -> None:
    number_of_monsters = random.randint(max_monsters//5, max_monsters)
    candidates = list(dungeon.swimmable_tiles)
    if len(candidates) > 0:
        for i in range(number_of_monsters):
            x, y = random.choice(candidates)
            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                monster_tables.sewer_water_table_1().spawn(dungeon, x, y)

def populate_sewer_sidewalk(dungeon: GameMap, max_monsters: int) -> None:
    number_of_monsters = random.randint(max_monsters//5, max_monsters)
    candidates = list(dungeon.walkable_tiles)
    if len(candidates) > 0:
        for i in range(number_of_monsters):
            x, y = random.choice(candidates)
            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                monster_tables.sewer_sidewalk_table_1().spawn(dungeon, x, y)

def populate_room(room:RectangularRoom, dungeon:GameMap) -> None:
    table = random.random()
    if table < 0.48:
        return
    elif table < 0.98:
        for i in range(random.randint(1,3)):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                monster_tables.sewer_room_table1().spawn(dungeon, x, y)
    else:
        for i in range(random.randint(5,15)):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                monster_tables.sewer_thief_hideout_table1().spawn(dungeon, x, y)

def generate_sewer_dungeon(
        max_tunnels: int,
        max_rooms: int,
        min_room_size: int,
        max_room_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
        seed,
) -> GameMap:

    random.seed(seed)
    np_seed(int(seed))
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, tile_types.sewer_wall, [player])

    """ first par of the algorithm generates rooms, these rooms.
    These rooms will be carved out once all room locations are determined"""
    #generating sewer tunnel rooms.
    rooms: List[(RectangularRoom, str)] = []
    if random.random() < 0.5: direction = 'h'
    else: direction = 'v'
    rooms.append(tunnel_sewer(dungeon, direction, random.randint(0, dungeon.width - 1), random.randint(0, dungeon.height - 1)))

    for r in range(max_tunnels):
        origin_room, origin_direction = random.choice(rooms)
        if origin_direction == 'h':
            direction = 'v'
            x, y = random.choice(list(origin_room.center_row_iterator))
        else:
            direction = 'h'
            x, y = random.choice(list(origin_room.center_column_iterator))
        new_room, new_dir = tunnel_sewer(dungeon, direction, x, y)
        if any((new_room.intersects(other_room) and new_dir == other_dir) for other_room, other_dir in rooms):
            continue
        rooms.append((new_room, direction))

    # generating rectangular rooms.
    connections : List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for r in range(max_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room, other_dir in rooms):
            continue #new_room intersects, and won't be used.

        connections.append((rooms[-1][0].center, new_room.center))
        rooms.append((new_room, 'r'))

    """Second part of the Algorithm caves out the rooms and populates them.
        Order of operaions is important to make sure that the map looks good, and that entities will be located where they should"""
    #carve the floors for the sewer tunnels.
    for room, direction in rooms:
        if direction != 'r':
            dungeon.tiles[room.inner] = np_choice(
                [tile_types.sewer_floor_clean, tile_types.sewer_floor_eroded, tile_types.sewer_floor_Rubble],
                (room.width - 1, room.height - 1), p=[0.9, 0.06, 0.04]
            )
    #carve sewege
    for room, direction in rooms:
        if  direction == 'h':
            dungeon.tiles[room.center_row] = np_choice([tile_types.sludge1, tile_types.sludge2, tile_types.sludge3], (1, room.width - 1), p=[0.1, 0.5, 0.4])
        elif direction == 'v':
            dungeon.tiles[room.center_column] = np_choice([tile_types.sludge1, tile_types.sludge2, tile_types.sludge3], (1, room.height - 1), p=[0.1, 0.50, 0.40])

    #add beidges over the sewege
    for room, direction in rooms:
        seg_start = None
        seg_end = None
        if direction == 'h':
            for r_x, r_y in room.center_row_iterator:
                if not seg_start:
                    seg_start = (r_x, r_y)
                if dungeon.tiles[r_x][r_y - 1]["swimmable"] or dungeon.tiles[r_x][r_y + 1]["swimmable"]:
                    seg_end = (r_x, r_y)
                if not dungeon.tiles[r_x + 1][r_y]["swimmable"]:
                    seg_end = (r_x, r_y)
                if seg_end:
                    if seg_start[0] + 1 < seg_end[0]:
                        dungeon.tiles[random.randint(seg_start[0] + 1, seg_end[0] - 1), r_y] = tile_types.floor_bridge
                    seg_start = seg_end
                    seg_end = None
        elif direction == 'v':
            for r_x, r_y in room.center_column_iterator:
                if not seg_start:
                    seg_start = (r_x, r_y)
                if dungeon.tiles[r_x - 1][r_y]["swimmable"] or dungeon.tiles[r_x + 1][r_y]["swimmable"]:
                    seg_end = (r_x, r_y)
                if not dungeon.tiles[r_x][r_y + 1]["swimmable"]:
                    seg_end = (r_x, r_y)
                if seg_end:
                    if seg_start[1] + 1 < seg_end[1]:
                        dungeon.tiles[r_x, random.randint(seg_start[1] + 1, seg_end[1] - 1)] = tile_types.floor_bridge
                    seg_start = seg_end
                    seg_end = None

    #populate the sewer tunnels
    populate_sewer_water(dungeon, 20)
    populate_sewer_sidewalk(dungeon, 20)

    #Carve and populate extra rooms
    for room, direction in rooms:
        if direction == 'r':
            dungeon.tiles[room.inner] = np_choice(
                [tile_types.sewer_floor_clean, tile_types.sewer_floor_eroded, tile_types.sewer_floor_Rubble],
                (room.width - 1, room.height - 1), p=[0.9, 0.06, 0.04]
            )
            populate_room(room, dungeon)

    player_x, player_y = random.choice(list(dungeon.walkable_tiles))
    blocker = dungeon.get_blocking_entity_at_location(player_x, player_y)
    if blocker:
        dungeon.entities.remove(blocker)
    player.place(player_x, player_y, dungeon)


    #carve small corridors.
    for start, end in connections:
        for x, y in tunnel_corridor(start, end):
            if not dungeon.tiles[x, y]["walkable"] and not dungeon.tiles[x, y]["swimmable"]:
                dungeon.tiles[x, y] = tile_types.small_corridor

    random.seed(None)
    np_seed(None)
    return dungeon

def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
        seed,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    random.seed(seed)
    np_seed(int(seed))

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width)
        y = random.randint(0, dungeon.height - room_height)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue #new_room intersects, and won't be used.

        dungeon.tiles[new_room.inner] = np_choice([tile_types.dungeon_floor_clean, tile_types.dungeon_floor_eroded, tile_types.dungeon_floor_Rubble],
                                                  (new_room.width - 1, new_room.height - 1), p=[0.9, 0.06, 0.04])
        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for x,y in tunnel_corridor(rooms[-1].center, new_room.center):
                if not dungeon.tiles[x, y]["walkable"] and not dungeon.tiles[x, y]["swimmable"]:
                    dungeon.tiles[x, y] = tile_types.dungeon_floor_eroded

        rooms.append(new_room)

    random.seed(None)
    np_seed(None)
    return dungeon