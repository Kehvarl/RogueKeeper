import libtcodpy as libtcod


def initialize_fov(game_map):
    """
    Create a new Field-Of-View map for the current game map
    :param Map.game_map.GameMap game_map:
    :return: fov_map
    """
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].block_move)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=libtcod.FOV_SHADOW):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
