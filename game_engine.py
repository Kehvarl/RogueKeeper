import libtcodpy as libtcod
from Components.creature import Creature
from Components.storage import Storage
from Entities.entity import Entity
from Map.map_functions import initialize_tiles, make_map, seed_ore
from Map.resource_functions import iron_ore
from Map.fov_function import initialize_fov, recompute_fov
from Map.game_map import GameMap
from UI.render_functions import render_all, clear_all
from input_handlers import handle_keys


def main():
    # Initial Game Settings
    screen_width = 80
    screen_height = 50
    # Map size
    map_width = 80
    map_height = 45
    # Field-Of-View settings
    fov_algorithm = libtcod.FOV_SHADOW
    fov_light_walls = True
    fov_radius = 10
    # Display-field colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130,110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Setup libtcod output console
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'Warrens', False)
    con = libtcod.console_new(screen_width, screen_height)

    # Initialize and generate game map
    game_map = GameMap(map_width, map_height, initialize_tiles)
    game_map = make_map(game_map, 5, 10, 20)
    seed_ore(game_map, iron_ore)

    # Field-of-view setup
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Initialize Player
    player = Entity(game_map.player_start_x, game_map.player_start_y, 'G', libtcod.white)
    player.add_component(Creature(25, 5, 5, 0))
    player.add_component(Storage('Inventory', 100))

    # Initialize test NPC
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    npc.add_component(Creature(10, 5, 5, 25))

    # Add starting entities to map
    game_map.entities = [npc, player]

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, game_map.entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        libtcod.console_flush()

        clear_all(con, game_map.entities)

        libtcod.console_put_char(con, player.x, player.y, ' ', libtcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        esc = action.get('esc')
        fullscreen = action.get('fullscreen')
        resources = None

        if move:
            dx, dy = move
            if game_map.point_in_map(player.x + dx, player.y + dy):
                if game_map.is_blocked(player.x + dx, player.y + dy):
                    resources = game_map.dig(player.x + dx, player.y + dy)
                    fov_map = initialize_fov(game_map)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

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
