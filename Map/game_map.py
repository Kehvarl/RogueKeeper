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

    def initialize_tiles(self):
        tiles = [[Tile(False) for _ in range(self.height)] for _ in range(self.width)]

        tiles[30][22].block_move = True
        tiles[30][22].block_sight = True
        tiles[31][22].block_move = True
        tiles[31][22].block_sight = True
        tiles[32][22].block_move = True
        tiles[32][22].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        return self.tiles[x][y].block_move
