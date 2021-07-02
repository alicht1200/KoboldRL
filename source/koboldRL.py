#!/usr/bin/env python3

import tcod
from source.actions import *
from source.input_handlers import EventHandler
from source.screen_definitions import ScrollType

from datetime import datetime
from os import getcwd
from os.path import join
import configparser

def main():
    screen_config = configparser.ConfigParser()
    screen_config.read('screen settings.ini')
    print (screen_config.sections())
    screen_width = int(screen_config['Resolution']['screen_width'])
    screen_height = int(screen_config['Resolution']['screen_height'])
    scroll_type = ScrollType[screen_config['Scrolling']['scroll_type']]
    scroll_margins = int(screen_config['Scrolling']['scroll_margins'])
    scroll_granularity = int(screen_config['Scrolling']['scroll_granularity'])
    screen_maximised = False


    # Following block belings in Dungeon Generation.
    dungeon_width = 100
    dungeon_height = 60
    player_x = dungeon_width // 2
    player_y = dungeon_height // 2

    game_font = tcod.tileset.load_tilesheet(path='resources/terminal16x16_gs_ro.png', rows=16, columns=16, charmap=tcod.tileset.CHARMAP_CP437)

    event_handler = EventHandler()

    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=game_font,
            title='Kobold RL',
            vsync=True
    ) as context:
        root_console = tcod.Console(width=screen_width, height=screen_height, order='F')

        blit_x = 0
        blit_y = 0
        dungeon_console = tcod.Console(width=dungeon_width, height=dungeon_height, order='F')
        while True:
            """
            Printing the screen
            """

            # Placing stuff will move to dungeon function later
            dungeon_console.print(dungeon_width//2, 0, 'N', fg=(200, 255, 255), bg_blend=tcod.BKGND_NONE)
            dungeon_console.print(dungeon_width//2, dungeon_height-1, 'S', fg=(200, 255, 255), bg_blend=tcod.BKGND_NONE)
            dungeon_console.print(0, dungeon_height//2, 'E', fg=(200, 255, 255), bg_blend=tcod.BKGND_NONE)
            dungeon_console.print(dungeon_width-1, dungeon_height//2, 'W', fg=(200, 255, 255), bg_blend=tcod.BKGND_NONE)

            dungeon_console.print(player_x, player_y, '@', fg=(255, 255, 255), bg_blend=tcod.BKGND_NONE)

            # Scrolling functionality.
            if scroll_type == ScrollType.GRANULARITY:
                if abs(blit_x - (player_x - screen_width//2)) > scroll_granularity:
                    blit_x = min(max(0, player_x - screen_width//2), dungeon_width - screen_width)
                if abs(blit_y - (player_y - screen_height // 2)) > scroll_granularity:
                    blit_y = min(max(0, player_y - screen_height//2), dungeon_height - screen_height)
            if scroll_type == ScrollType.SCREEN_EDGE:
                if abs(blit_x - (player_x - screen_width//2)) > abs((screen_width//2) - scroll_margins):
                    blit_x = min(max(0, player_x - screen_width//2), dungeon_width - screen_width)
                if abs(blit_y - (player_y - screen_height//2)) > abs((screen_height//2) - scroll_margins):
                    blit_y = min(max(0, player_y - screen_height//2), dungeon_height - screen_height)

            dungeon_console.blit(root_console, 0, 0, blit_x, blit_y, screen_width, screen_height)
            context.present(root_console,integer_scaling=True)
            dungeon_console.clear()



            """
            event handlers
            """
            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue
                # game actions
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                # Misc Actions
                elif isinstance(action, EscapeAction):
                    raise SystemExit()
                elif isinstance(action, ScreenShotAction):
                    context.save_screenshot(join(getcwd(), f'ScreenShot_{datetime.now().timestamp()}.png'))
                # Screen related Actions
                elif isinstance(action, FullScreenAction):
                    screen_maximised = True
                    tcod.lib.SDL_SetWindowFullscreen(
                        context.sdl_window_p,
                        tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP if action.FullScreen else 0
                    )
                    tcod.lib.SDL_SetWindowSize(context.sdl_window_p, screen_width * 16, screen_height * 16)
                elif isinstance(action, ResizeAction):
                    screen_width, screen_height = context.recommended_console_size(1,1)
                    if not screen_maximised:
                        tcod.lib.SDL_SetWindowSize(
                            context.sdl_window_p,
                            screen_width * 16, screen_height * 16)
                    else:
                        screen_maximised = False
                    root_console = context.new_console(1, 1)
                elif isinstance(action, MaximiseAction):
                    screen_maximised = True


if __name__ == '__main__':
    main()