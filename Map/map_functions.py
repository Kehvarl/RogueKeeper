import libtcodpy as libtcod
from random import randint

from Entities.entity import Entity
from Map.room import Room
from Map.tile import Tile
from UI.render_functions import RenderOrder


def initialize_tiles(game_map, default_block_move=True, default_block_sight=True,
                     default_hardness=1):
    """
    Set the initial tile-state for a new map
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param bool default_block_move:  Tiles block movement by default
    :param bool default_block_sight:  Tiles block sight by default
    :param int default_hardness: How difficult it is to carve through this material
    :return list: Tiles that make up the map
    """
    tiles = [
        [Tile(block_move=default_block_move,
              block_sight=default_block_sight,
              hardness=default_hardness)
         for _ in range(game_map.height)]
        for _ in range(game_map.width)]

    return tiles


def make_map(game_map, max_rooms=1, room_min_size=5, room_max_size=10,
             max_monsters_per_room=3):
    """
    Create initial Map Layout
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param int max_rooms: Number of rooms to attempt to generate
    :param int room_min_size: Smallest allowable room (width or height)
    :param int room_max_size: Largest allowable room (width or height)
    :param int max_monsters_per_room: Maximum number of Entities to spawn in a room
    """
    num_rooms = 0

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, game_map.width - w - 1)
        y = randint(0, game_map.height - h - 1)

        # Room class stores some useful features
        new_room = Room(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        for other_room in game_map.rooms:
            if new_room.intersect(other_room):
                break
        else:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(game_map, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                game_map.player_start_x = new_x
                game_map.player_start_y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = game_map.rooms[num_rooms - 1].center()

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

                place_entities(game_map, new_room, max_monsters_per_room)

            # finally, append the new room to the list
            game_map.rooms.append(new_room)
            num_rooms += 1
    return game_map


def create_room(game_map, room):
    """
    Set the tiles of a room to be passable
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param Map.room.Room room: The room in the map
    """
    # Make walls harder to dig through
    for x in range(room.x1, room.x2+1):
        game_map.tiles[x][room.y1].hardness = 500
        game_map.tiles[x][room.y2].hardness = 500
    for y in range(room.y1, room.y2+1):
        game_map.tiles[room.x1][y].hardness = 500
        game_map.tiles[room.x2][y].hardness = 500
    # Make interior tiles passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.tiles[x][y].clear()


def create_h_tunnel(game_map, x1, x2, y):
    """
    Create a horizontal tunnel between two points
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param int x1: starting x coordinate
    :param int x2: ending x coordinate
    :param int y: y coordinate for both point
    """
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.tiles[x][y].clear()


def create_v_tunnel(game_map, y1, y2, x):
    """
    Create a vertical tunnel between two points
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param int y1: starting y coordinate
    :param int y2: ending y coordinate
    :param int x: x coordinate for both points
    """
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.tiles[x][y].clear()


def seed_ore(game_map, ore_function=None):
    """
    Scatter resources around the map
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param Callable ore_function: resource-generation function
    """
    for ore in range(randint(10, 25)):
        x = randint(0, game_map.width - 1)
        y = randint(0, game_map.height - 1)
        create_ore_vein(game_map, x, y, ore_function)


def create_ore_vein(game_map, x, y, ore_function):
    """
    Spread ore using Random-Walk
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param int x: starting position
    :param int y: starting position
    :param Callable ore_function: minable_resource function
    """
    current_x = x
    current_y = y
    for steps in range(randint(5, 50)):
        if 0 < current_y < game_map.height and 0 < current_x < game_map.width:
            if game_map.tiles[current_x][current_y].hardness > 0:
                game_map.tiles[current_x][current_y].resources.append(ore_function)
        current_x += randint(-1, 1)
        current_y += randint(-1, 1)


def place_entities(game_map, room, max_monsters_per_room):
    """
    Add monsters to a room in the game_map
    :param Map.game_map.GameMap game_map: The game map being worked with
    :param Map.room.Room room: Map room to add monsters to
    :param int max_monsters_per_room: Maximum number of Entities to spawn in the room
    """
    # Get a random number of monsters
    number_of_monsters = randint(0, max_monsters_per_room)

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in game_map.entities if entity.x == x and entity.y == y]):
            if randint(0, 100) < 80:
                monster = Entity(x, y, 'k', libtcod.desaturated_green, "Kobold",
                                 blocks=True, render_order=RenderOrder.ACTOR)
            else:
                monster = Entity(x, y, 's', libtcod.darker_green, "Skeleton",
                                 blocks=True, render_order=RenderOrder.ACTOR)

            game_map.entities.append(monster)
