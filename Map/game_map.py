from random import randint

from Map.tile import Tile
from Map.room import Room
from Map.resource_functions import iron_ore


class GameMap:
    """
    Represents a complete Game Map and all the Tiles on it
    """
    def __init__(self, width, height):
        """
        Create a new map
        :param int width: Size of map in Tiles
        :param int height: Size of map in Tiles
        """
        self.width = width
        self.height = height
        self.player_start_x = int(width / 2)
        self.player_start_y = int(height / 2)
        self.tiles = self.initialize_tiles()
        self.rooms = []
        self.entities = []

    def initialize_tiles(self, default_block_move=True, default_block_sight=True,
                         default_hardness=1):
        """
        Set the initial tilestate for a new map
        :param bool default_block_move:  Tiles block movement by default
        :param bool default_block_sight:  Tiles block sight by default
        :param int default_hardness: How difficult it is to carve through this material
        :return list: Tiles that make up the map
        """
        tiles = [
            [Tile(block_move=default_block_move,
                  block_sight=default_block_sight,
                  hardness=default_hardness)
             for _ in range(self.height)]
            for _ in range(self.width)]

        return tiles

    def make_map(self, max_rooms=1, room_min_size=5, room_max_size=10):
        """
        Create initial Map Layout
        :param int max_rooms: Number of rooms to attempt to generate
        :param int room_min_size: Smallest allowable room (width or height)
        :param int room_max_size: Largest allowable room (width or height)
        """
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Room(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    self.player_start_x = new_x
                    self.player_start_y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = self.rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1

    def seed_ore(self):
        """
        Scatter resources around the map
        """
        for ore in range(randint(10,25)):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            self.create_ore_vein(x, y, iron_ore)

    def create_ore_vein(self, x, y, ore_function):
        current_x = x
        current_y = y
        for steps in range(randint(5, 50)):
            if 0 < current_y < self.height and 0 < current_x < self.width:
                if self.tiles[current_x][current_y].hardness > 0:
                    self.tiles[current_x][current_y].resources.append(ore_function)
            current_x += randint(-1, 1)
            current_y += randint(-1, 1)

    def create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Map.room.Room room: The room in the map
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].clear()

    def create_h_tunnel(self, x1, x2, y):
        """
        Create a horizontal tunnel between two points
        :param int x1: starting x coordinate
        :param int x2: ending x coordinate
        :param int y: y coordinate for both point
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].clear()

    def create_v_tunnel(self, y1, y2, x):
        """
        Create a vertical tunnel between two points
        :param int y1: starting y coordinate
        :param int y2: ending y coordinate
        :param int x:  x coordinate for both points
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].clear()

    def dig(self, x, y, strength=1):
        """
        Try to tunnel into a Tile, may result in ore and treasure
        :param int x: position of Tile on map
        :param int y: position of Tile on map
        :param int strength: Speed at which a tile is carved through.
        :return dict: Type and Quantity of anything dug up
        """
        return self.tiles[x][y].dig(strength)

    def is_blocked(self, x, y):
        """
        Check if a tile blocks movement
        :param int x: Tile Position
        :param int y: Tile Position
        :return bool: True if tile blocks movement.
        """
        return self.tiles[x][y].block_move
