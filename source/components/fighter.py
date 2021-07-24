"""
This component should handle fighting capabilities for entities.
Any entity capable participate in combat will have this.
"""

from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from source.components.base_component import BaseComponent
from source.render_order import RenderOrder
from source.input_handlers import GameOverEventHandler

if TYPE_CHECKING:
    from source.entity import Actor

class Fighter(BaseComponent):
    entity: Actor

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
        if self._hp == 0 and self.entity.ai:
            self.dies()

    def dies(self) -> None:
        if self.engine.player is self.entity:
            death_message = 'You died!'
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f'{self.entity.name.capitalize()} is dead!'

        self.entity.char = '%'
        self.entity.color = (150, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f'{self.entity.name}\'s corpse'
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)