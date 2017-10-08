import libtcodpy as libtcod
from Entities.entity import Entity
from Components.creature import Creature
from Components.storage import Storage
from input_handlers import handle_keys
from UI.render_functions import render_all, clear_all
from Map.game_map import GameMap


def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'Warrens', False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(5, 10, 20)

    player_x = game_map.player_start_x
    player_y = game_map.player_start_y

    player = Entity(player_x, player_y, 'G', libtcod.white)
    player.add_component(Creature(25, 5, 5, 0))
    player.add_component(Storage('Inventory', 100))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    npc.add_component(Creature(10, 5, 5, 25))
    game_map.entities = [npc, player]
    game_map.seed_ore()

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, game_map.entities, game_map, screen_width, screen_height, colors)

        libtcod.console_flush()

        clear_all(con, game_map.entities)

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        esc = action.get('esc')
        fullscreen = action.get('fullscreen')
        resources = None

        if move:
            dx, dy = move
            if game_map.is_blocked(player.x + dx, player.y + dy):
                resources = game_map.dig(player.x + dx, player.y + dy)
            else:
                player.move(dx, dy)

        if resources:
            for resource in resources:
                status_list = player.components['Inventory'].add_resource(resource)
                for status in status_list:
                    if status.get('item_status', 'none') == 'rejected':
                        resource_drop = Entity(player.x, player.y, '$', libtcod.white,
                                               resource=resource)
                        game_map.entities.append(resource_drop)

        if esc:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
