import libtcodpy as libtcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    """
    Draw all the entities in the map
    :param con: Console to draw on
    :param list entities: All the Entities on the map
    :param Map.game_map.GameMap game_map: Map of the current level
    :param fov_map: Field-Of-View map overlay
    :param bool fov_recompute: Redraw visible area (FOV has changed)
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    :param dict colors: Colors for the current level
    """

    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                else:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw all the entities in the game map
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    """
    Clear current position of all entities in the map
    :param con: Console to draw on
    :param list entities: All the Entities on the map
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    """
    Draw the character representing the given Entity
    :param con: Console to draw on
    :param Entities.entity.Entity entity: The Entity to draw
    """
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """
    Erase the character representing the given Entity
    :param con: Console to draw on
    :param Entities.entity.Entity entity: The Entity to clear
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)