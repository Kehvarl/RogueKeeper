class GameMap:
    """
    Represents a complete Game Map and all the Tiles on it
    """

    def __init__(self, width, height, initialize_tiles):
        """
        Create a new map
        :param int width: Size of map in Tiles
        :param int height: Size of map in Tiles
        """
        self.width = width
        self.height = height
        self.player_start_x = int(width / 2)
        self.player_start_y = int(height / 2)
        self.tiles = initialize_tiles(self)
        self.rooms = []
        self.entities = []

    def point_in_map(self, x, y):
        """
        Checks if a given point falls within the current map
        :param x: Target X position
        :param y: Target Y position
        :return: True if desired location is within map bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

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
        :param int x: position of Tile on map
        :param int y: position of Tile on map
        :return bool: True if tile blocks movement.
        """
        return self.tiles[x][y].block_move

    def get_blocking_entities_at_location(self, x, y):
        """
        Check for Entities that block movement at a given point
        :param int x: position to check for Entities
        :param int y: position to check for Entities
        :return: Blocking Entity or None if no blocking entities
        """
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return entity
        return None
