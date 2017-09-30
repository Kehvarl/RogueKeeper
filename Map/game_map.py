from Map.tile import Tile
from Map.room import Room


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
        self.tiles = self.initialize_tiles()

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

    def make_map(self):
        """
        Create initial Map Layout
        """
        room1 = Room(10, 15, 10, 15)
        room2 = Room(35, 15, 10, 15)
        self.create_room(room1)
        self.create_room(room2)

    def create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Map.room.Room room: The room in the map
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block_move = False
                self.tiles[x][y].block_sight = False

    def dig(self, x, y, strength=1):
        """
        Try to tunnel into a Tile
        :param int x: position of Tile on map
        :param int y: position of Tile on map
        :param int strength: Speed at which a tile is carved through.
        """
        self.tiles[x][y].dig(strength)

    def is_blocked(self, x, y):
        """
        Check if a tile blocks movement
        :param int x: Tile Position
        :param int y: Tile Position
        :return bool: True if tile blocks movement.
        """
        return self.tiles[x][y].block_move
