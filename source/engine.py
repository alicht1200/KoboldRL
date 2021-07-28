from __future__ import annotations
from typing import TYPE_CHECKING

from tcod import lib
from tcod.context import  Context
from tcod.console import Console
from tcod.context import SDL_WINDOW_FULLSCREEN_DESKTOP
from tcod.map import compute_fov


from os import getcwd
from os.path import join
from datetime import datetime

from source.input_handlers import MainGameEventHandler
from source.message_log import  MessageLog
from source.render_functions import render_bar, render_names_at_mouse_location
if TYPE_CHECKING:
    from source.entity import Actor
    from source.game_map import GameMap
    from source.input_handlers import EventHandler

from source.screen_definitions import ScrollType

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor, context: Context, root_console: Console, scroll_type: ScrollType, scroll_value: int):
        self.event_handler : EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.player = player
        self.context = context
        self.root_console = root_console
        self.screen_maximised = False
        self.scroll_type = scroll_type
        self.scroll_value = scroll_value
        self.console_x = 0
        self.console_y = 0

    def handle_enemy_turns(self)-> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def take_screenshot(self)->None:
        self.context.save_screenshot(join(getcwd(), f'ScreenShot_{datetime.now().timestamp()}.png'))

    def screen_resize(self)->None:
        screen_width, screen_height = self.context.recommended_console_size(1, 1)
        if not self.screen_maximised:
            lib.SDL_SetWindowSize(
                self.context.sdl_window_p,
                screen_width * 16, screen_height * 16)
        else:
            self.screen_maximised = False
        self.root_console = self.context.new_console(1, 1)

    def set_fullscreen(self, full_screen)->None:
        self.screen_maximised = True
        lib.SDL_SetWindowFullscreen(
            self.context.sdl_window_p,
            SDL_WINDOW_FULLSCREEN_DESKTOP if full_screen else 0
        )
        lib.SDL_SetWindowSize(self.context.sdl_window_p, self.root_console.width * 16, self.root_console.height * 16)

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is 'visible' it should be added to 'explored'
        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console) -> None:
        screen_width = self.root_console.width
        screen_height = self.root_console.height - 7
        self.game_map.render(console)

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
        # self.root_console.print(x=0, y=screen_height, string=f'seed = {seed}')
        self.message_log.render(console=self.root_console, x=21, y=screen_height + 1, width=screen_width - 22, height=self.root_console.height - screen_height)
        render_bar(console=self.root_console, current_value=self.player.fighter.hp, maximum_value=self.player.fighter.max_hp, total_width=20)

        render_names_at_mouse_location(console=self.root_console, x=21, y=screen_height, engine=self)