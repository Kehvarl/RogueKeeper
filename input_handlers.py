import libtcodpy as libtcod


def handle_keys(key):
    # Movement keys
    if key.vk == libtcod.KEY_UP:
        return _move(0, -1)
    elif key.vk == libtcod.KEY_DOWN:
        return _move(0, 1)
    elif key.vk == libtcod.KEY_LEFT:
        return _move(-1, 0)
    elif key.vk == libtcod.KEY_RIGHT:
        return _move(1, 0)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'esc': True}

    # No key was pressed
    return {}


def _move(dx=0, dy=0):
    return {'move': (dx, dy)}
