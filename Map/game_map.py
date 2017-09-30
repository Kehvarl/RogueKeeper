from Map.tile import Tile


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

    def initialize_tiles(self, default_block_move=True, default_block_sight=False):
        """
        Set the initial tile-state for a new map
        :param bool default_block_move:  Tiles block movement by default
        :param bool default_block_sight:  Tiles block sight by default
        :return list: Tiles that make up the map
        """
        tiles = [[Tile(default_block_move, default_block_sight)
                  for _ in range(self.height)]
                 for _ in range(self.width)]

        return tiles

    def create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Map.room.Room room: The room in the map
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block_move = False
                self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        """
        Check if a tile blocks movement
        :param int x: Tile Position
        :param int y: Tile Position
        :return bool: True if tile blocks movement.
        """
        return self.tiles[x][y].block_move
