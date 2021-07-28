"""
This component should handle fighting capabilities for entities.
Any entity capable participate in combat will have this.
"""

from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

import source.color as color
from source.components.base_component import BaseComponent
from source.render_order import RenderOrder
from source.input_handlers import GameOverEventHandler

if TYPE_CHECKING:
    from source.entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, dodge: int, resistance: int, accuracy: int, damage: Tuple[int, int]):
        self.max_hp = hp
        self._hp = hp
        self.dodge = dodge
        self.resistance = resistance
        self.accuracy = accuracy
        self.damage = damage

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.dies()

    def dies(self) -> None:
        if self.engine.player is self.parent:
            death_message = 'You died!'
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f'{self.parent.name.capitalize()} is dead!'
            death_message_color = color.enemy_die

        self.parent.char = '%'
        self.parent.color = (150, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f'{self.parent.name}\'s corpse'
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)