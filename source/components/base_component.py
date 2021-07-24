from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.engine import Engine
    from source.entity import Entity

class BaseComponent:
    entity: Entity #Owning entity instance.

    @property
    def engine(self) -> Engine:
        return self.entity.game_map.engine