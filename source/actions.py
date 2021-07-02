class Action:
    pass

################
# Window Actions
################

class EscapeAction(Action):
    pass

class ScreenShotAction(Action):
    pass

class ResizeAction(Action):
    pass

class FovActiveAction(Action):
    FovActive = True

    def __init__(self):
        FovActiveAction.FovActive = not FovActiveAction.FovActive

class MaximiseAction(Action):
    pass

# This method tracks full screen with a Class variable, but it means that it will aways start as False.
# Consider having it read from input instead.
class FullScreenAction(Action):
    FullScreen = False

    def __init__(self):
        FullScreenAction.FullScreen = not FullScreenAction.FullScreen

##############
# Game Actions
##############
class MovementAction(Action):

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy