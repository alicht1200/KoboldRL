#!/usr/bin/env python3

import tcod
from source.actions import EscapeAction, MovementAction, FullScreenAction
from source.input_handlers import EventHandler


def main():
    # need to be read from a file
    sccreen_width = 100
    sccreen_height = 60

    player_x = sccreen_width // 2
    player_y = sccreen_height // 2

    game_font = tcod.tileset.load_tilesheet(path='resources/terminal16x16_gs_ro.png', rows=16, columns=16, charmap=tcod.tileset.CHARMAP_CP437)

    event_handler = EventHandler()

    with tcod.context.new(
            columns=sccreen_width,
            rows=sccreen_height,
            tileset=game_font,
            title='Kobold RL',
            vsync=True
    ) as context:
        root_console = tcod.Console(width=sccreen_width, height=sccreen_height, order='F')
        while True:
            """
            Printing the screen
            """
            root_console.print(player_x, player_y, '@', fg=(255, 255, 255), bg_blend=tcod.BKGND_NONE)
            context.present(root_console)
            root_console.clear()

            """
            event handlers
            """
            for event in tcod.event.get():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                elif isinstance(action, EscapeAction):
                    raise SystemExit()
                elif isinstance(action, FullScreenAction):
                    tcod.lib.SDL_SetWindowFullscreen(
                        context.sdl_window_p,
                        tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP if action.FullScreen else 0
                    )


if __name__ == '__main__':
    main()