from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from source.render_order import RenderOrder

if TYPE_CHECKING:
    from source.components.ai import BaseAI
    from source.components.fighter import Fighter
    from source.game_map import GameMap

    T = TypeVar('T', bound='Entity')

class Entity:
    """
    A generic object representing any dynamic entity such as Player, Enemies, items etc.
    """

    parent : GameMap

    def __init__(
            self,
            *,
            parent: Optional[GameMap] = None,
            x:int = 0,
            y:int = 0,
            char:str = '?',
            color:Tuple[int, int, int] = (255, 255, 255),
            name:str = '<unnamed>',
            blocks_movement:bool = False,
            render_order: RenderOrder = RenderOrder.CORPSE
                ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def game_map(self) -> GameMap:
        return  self.parent.game_map

    def spawn(self: T, game_map:GameMap, x:int, y:int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x:int, y:int, game_map:Optional[GameMap]) -> None:
        """Place this entity at a new location.  Handles moving across game_maps."""
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "parent"): # Possibly uninitialized.
                if self.parent is self.game_map:
                    self.game_map.entities.remove(self)
            self.parent = game_map
            game_map.entities.add(self)

    def move(self, dx:int, dy:int) -> None:
        #Move the entity by a given amount
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = '?',
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = '<Unnamed>',
            walks: bool = False,
            swims: bool = False,
            small: bool = False,
            ai_cls: Type[BaseAI],
            fighter: Fighter
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )
        self.walks = walks
        self.swims = swims
        self.small = small
        self.ai: Optional[BaseAI] = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return  bool(self.ai)
