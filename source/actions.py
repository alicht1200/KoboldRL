from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from source.engine import Engine
    from source.entity import Actor, Entity

class Action:
    def __init__(self, entity:Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) ->Engine:
        """Return the engine this action belongs to."""
        return self.entity.game_map.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


################
# Window Actions
################

class ScreenShotAction(Action):

    def perform(self) -> None:
        self.engine.take_screenshot()

class ResizeAction(Action):

    def perform(self) -> None:
        self.engine.screen_resize()

class FovActiveAction(Action):
    FovActive = True

    def perform(self) -> None:
        pass

    def __init__(self):
        FovActiveAction.FovActive = not FovActiveAction.FovActive

class MaximiseAction(Action):

    def perform(self, ) -> None:
        self.engine.screen_maximised = True

# This method tracks full screen with a Class variable, but it means that it will aways start as False.
# Consider having it read from input instead.
class FullScreenAction(Action):
    FullScreen = False

    def perform(self, engine: Engine, entity: Entity) -> None:
        FullScreenAction.FullScreen = not FullScreenAction.FullScreen
        engine.set_fullscreen(FullScreenAction.FullScreen)

##############
# Game Actions
##############

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class WaitAction(Action):
    def perform(self) -> None:
        pass

class ActionWithDirection(Action):
    def __init__(self, entity:Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self)->Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        attacker = self.entity
        target = self.target_actor
        if not target:
            return  #no entity to attack
        print(f'{attacker.name.capitalize()} attaks {target.name.capitalize()}, ', end='')
        roll = random.randint(1, 20)
        if (roll + attacker.fighter.accuracy) < target.fighter.dodge and roll < 20:
            print(f'and misses.')
            return
        damage = random.randint(*attacker.fighter.damage) - target.fighter.resistance
        print(f'and Hits! ', end='')
        if damage <= 0:
            print(f'but fails to do any damage...')
            return
        print(f'causing {damage} hit points in damage')
        target.fighter.hp -= damage



class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return #Destination is out of bounds
        if not ((self.engine.game_map.tiles["walkable"][dest_x, dest_y] and self.entity.walks)
                or (self.engine.game_map.tiles["swimmable"][dest_x, dest_y] and self.entity.swims)):
            return  #Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  #destination is blocked by entity
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()