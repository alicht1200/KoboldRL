from typing import Set, Iterable, Any

from tcod import lib
from tcod.context import  Context
from tcod.console import Console
from tcod.context import SDL_WINDOW_FULLSCREEN_DESKTOP


from os import getcwd
from os.path import join
from datetime import datetime


from source.actions import *
from source.entity import Entity
from source.game_map import GameMap
from source.input_handlers import EventHandler
from source.screen_definitions import ScrollType

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity, root_console: Console, scroll_type: ScrollType, scroll_value: int):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.root_console = root_console
        self.screen_maximised = False
        self.scroll_type = scroll_type
        self.scroll_value = scroll_value
        self.console_x = 0
        self.console_y = 0

    def handle_events(self, events: Iterable[Any], context: Context) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            elif isinstance(action, ScreenShotAction):
                context.save_screenshot(join(getcwd(), f'ScreenShot_{datetime.now().timestamp()}.png'))

            # Screen related Actions
            elif isinstance(action, FullScreenAction):
                self.screen_maximised = True
                lib.SDL_SetWindowFullscreen(
                    context.sdl_window_p,
                    SDL_WINDOW_FULLSCREEN_DESKTOP if action.FullScreen else 0
                )
                lib.SDL_SetWindowSize(context.sdl_window_p, self.root_console.width * 16, self.root_console.height * 16)
            elif isinstance(action, ResizeAction):
                screen_width, screen_height = context.recommended_console_size(1, 1)
                if not self.screen_maximised:
                    lib.SDL_SetWindowSize(
                        context.sdl_window_p,
                        screen_width * 16, screen_height * 16)
                else:
                    self.screen_maximised = False
                self.root_console = context.new_console(1, 1)


            action.perform(self, self.player)


    def render(self, console: Console, context: Context, seed) -> None:
        screen_width = self.root_console.width
        screen_height = self.root_console.height - 5
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, entity.color)

        # handle screen scroll   #
        if self.scroll_type == ScrollType.GRANULARITY:
            if (console.width > screen_width ) and abs(self.console_x - (self.player.x - screen_width//2)) > self.scroll_value:
                self.console_x = min(max(0, self.player.x - screen_width//2), console.width - screen_width)
            if (console.width > screen_height ) and abs(self.console_y - (self.player.y - screen_height // 2)) > self.scroll_value:
                self.console_y = min(max(0, self.player.y - screen_height//2), console.height - screen_height)
        if self.scroll_type == ScrollType.SCREEN_EDGE:
            if (console.width > screen_width ) and abs(self.console_x - (self.player.x - screen_width//2)) > abs((screen_width//2) - self.scroll_value):
                self.console_x = min(max(0, self.player.x - screen_width//2), console.width - screen_width)
            if (console.width > screen_height ) and abs(self.console_y - (self.player.y - screen_height//2)) > abs((screen_height//2) - self.scroll_value):
                self.console_y = min(max(0, self.player.y - screen_height//2), console.height - screen_height)
        ##########################
        console.blit(self.root_console, 0, 0, self.console_x, self.console_y, screen_width, screen_height)
        self.root_console.print(x=0, y=56, string=f'seed = {seed}')
        context.present(self.root_console,integer_scaling=True)
        console.clear()