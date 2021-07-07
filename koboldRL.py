#!/usr/bin/env python3

import tcod

import configparser

from source.engine import Engine
from source.input_handlers import EventHandler
from source.entity import Entity
from source.game_map import GameMap
from source.screen_definitions import ScrollType

def main():
    screen_config = configparser.ConfigParser()
    screen_config.read('screen settings.ini')
    screen_width = int(screen_config['Resolution']['screen_width'])
    screen_height = int(screen_config['Resolution']['screen_height'])
    scroll_type = ScrollType[screen_config['Scrolling']['scroll_type']]
    scroll_tiles = int(screen_config['Scrolling']['scroll_tiles'])


    # Following block belongs in Dungeon Generation.
    dungeon_width = 100
    dungeon_height = 55

    game_font = tcod.tileset.load_tilesheet(path='resources/terminal16x16_gs_ro.png', rows=16, columns=16, charmap=tcod.tileset.CHARMAP_CP437)

    event_handler = EventHandler()

    player = Entity((dungeon_width // 2), (dungeon_height // 2), "@", (255, 255, 255))
    npc = Entity((dungeon_width // 2 - 4), (dungeon_height // 2), "@", (200, 200, 10))
    entities = {npc, player}

    game_map = GameMap(dungeon_width, dungeon_height)

    root_console = tcod.Console(width=screen_width, height=screen_height, order='F')
    engine = Engine(entities, event_handler, game_map, player, root_console, scroll_type, scroll_tiles)

    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=game_font,
            title='Kobold RL',
            vsync=True
    ) as context:

        dungeon_console = tcod.Console(width=dungeon_width, height=dungeon_height, order='F')
        while True:

            engine.render(dungeon_console, context)

            events = tcod.event.get()
            engine.handle_events(events, context)



if __name__ == '__main__':
    main()