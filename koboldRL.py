#!/usr/bin/env python3

import configparser
from datetime import datetime
import copy

import tcod

from source.engine import Engine
from source.entity import Entity
from source.input_handlers import EventHandler
# from source.game_map import GameMap
from source.map_generation.dungeon_gen import generate_sewer_dungeon
import source.map_generation.entity_factories as entity_list
from source.screen_definitions import ScrollType


def main():
    screen_config = configparser.ConfigParser()
    screen_config.read('screen settings.ini')
    screen_width = int(screen_config['Resolution']['screen_width'])
    screen_height = int(screen_config['Resolution']['screen_height'])
    scroll_type = ScrollType[screen_config['Scrolling']['scroll_type']]
    scroll_tiles = int(screen_config['Scrolling']['scroll_tiles'])
    seed =datetime.now().timestamp()
    print(seed) # TODO: remove this in prodiction.


    # Following block belongs in Dungeon Generation.
    dungeon_width = 100
    dungeon_height = 55
    dungeon_room_max_size = 14
    dungeon_room_min_size = 6
    max_dungeon_rooms = 30
    max_sewer_tunnels = 20

    game_font = tcod.tileset.load_tilesheet(path='resources/terminal16x16_gs_ro.png', rows=16, columns=16, charmap=tcod.tileset.CHARMAP_CP437)

    event_handler = EventHandler()

    player = copy.deepcopy(entity_list.player)


    game_map = generate_sewer_dungeon(
        max_tunnels= max_sewer_tunnels,
        max_rooms= max_dungeon_rooms,
        map_width=dungeon_width,
        map_height=dungeon_height,
        min_room_size= dungeon_room_min_size,
        max_room_size=dungeon_room_max_size,
        player=player,
        seed=seed
    )

    root_console = tcod.Console(width=screen_width, height=screen_height, order='F')
    engine = Engine(event_handler, game_map, player, root_console, scroll_type, scroll_tiles)

    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=game_font,
            title='Kobold RL',
            vsync=True
    ) as context:

        dungeon_console = tcod.Console(width=dungeon_width, height=dungeon_height, order='F')
        while True:

            engine.render(dungeon_console, context, seed)

            events = tcod.event.get()
            engine.handle_events(events, context)


if __name__ == '__main__':
    main()