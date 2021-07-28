#!/usr/bin/env python3

import configparser
from datetime import datetime
import copy

import tcod

import  source.color as color
from source.engine import Engine
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





    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=game_font,
            title='Kobold RL',
            vsync=True
    ) as context:
        player = copy.deepcopy(entity_list.player)
        root_console = tcod.Console(width=screen_width, height=screen_height, order='F')
        engine = Engine(player=player, context=context, root_console=root_console, scroll_type=scroll_type, scroll_value=scroll_tiles)

        engine.game_map = generate_sewer_dungeon(
            max_tunnels=max_sewer_tunnels,
            max_rooms=max_dungeon_rooms,
            map_width=dungeon_width,
            map_height=dungeon_height,
            min_room_size=dungeon_room_min_size,
            max_room_size=dungeon_room_max_size,
            engine=engine,
            seed=seed
        )

        engine.update_fov()

        engine.message_log.add_message(
            "Treacherous gnomes have stole several eggs from the hachery! It's your mission to retrive the lost eggs, else who knows what the gnomes will do with them?",
            color.welcome_text
        )

        dungeon_console = tcod.Console(width=dungeon_width, height=dungeon_height, order='F')
        while True:
            # dungeon_console.clear()
            engine.root_console.clear()
            engine.event_handler.on_render(console=dungeon_console)
            context.present(engine.root_console)
            engine.event_handler.handle_events(context)


if __name__ == '__main__':
    main()