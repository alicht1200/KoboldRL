from tcod import tileset as tcod_tileset
from tcod import Console as tcod_Console
from tcod import context as tcod_context
from tcod import event as tcod_event
from tcod import  BKGND_NONE

from Source.input_handlers import handle_keys


def main():
    # need to be read from a file
    sccreen_width = 100
    sccreen_height = 60

    player_x = sccreen_width // 2
    player_y = sccreen_height // 2

    game_font = tcod_tileset.load_tilesheet(path='resources/terminal16x16_gs_ro.png', rows=16, columns=16, charmap=tcod_tileset.CHARMAP_CP437)
    console =  tcod_Console(width=sccreen_width, height=sccreen_height, order='F')
    with tcod_context.new(columns=console.width, rows=console.height, tileset=game_font) as context:
        while True:
            """
            Printing the screen
            """
            console.clear()
            console.print(player_x, player_y, '@', fg=(255, 255, 255), bg_blend=BKGND_NONE)
            context.present(console)

            """
            event handlers
            """
            for event in tcod_event.get():
                context.convert_event(event)
                action = handle_keys(event)

                move = action.get('move')
                exit = action.get('exit')

                if move:
                    dx, dy = move
                    player_x += dx
                    player_y += dy

                if event.type == "QUIT" or exit:
                    raise SystemExit()


if __name__ == '__main__':
    main()