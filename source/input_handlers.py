from typing import Optional

import tcod.event

from  source.actions import *


class EventHandler(tcod.event.EventDispatch[Action]):

    def ev_quit(self, event: "tcod.event.Quit") -> Optional[Action]:
        raise SystemExit()

    def ev_windowresized(self, event: "tcod.event.WindowResized"):
        return ResizeAction()

    def ev_windowmaximized(self, event: "tcod.event.WindowEvent"):
        return MaximiseAction()

    def ev_keydown(self, event: "tcod.event.KeyDown") -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        mod = event.mod

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        elif key == tcod.event.K_F12:
            action = ScreenShotAction()

        elif key == tcod.event.K_RETURN and (mod & tcod.event.Modifier.ALT) != 0:
            action = FullScreenAction()

        return action