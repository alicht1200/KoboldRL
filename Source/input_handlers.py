from tcod.event import Modifier
from tcod.event import KeySym as tcod_KeySym

def handle_keys(key):

    if key.type == 'KEYDOWN':
        if key.sym == tcod_KeySym.UP:
            return {'move': (0, -1)}
        if key.sym == tcod_KeySym.DOWN:
            return {'move': (0, 1)}
        if key.sym == tcod_KeySym.LEFT:
            return {'move': (-1, 0)}
        if key.sym == tcod_KeySym.RIGHT:
            return {'move': (1, 0)}

        if key.mod & Modifier.ALT and key.sym == tcod_KeySym.RETURN:

            return {'full screen': True}
        if key.sym == tcod_KeySym.ESCAPE:
            return {'exit': True}
    return {}