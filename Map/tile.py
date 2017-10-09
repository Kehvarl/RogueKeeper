class Tile:
    """
    A tile on the map
    """
    def __init__(self, block_move=True, block_sight=None, hardness=1):
        """
        Create a new Tile
        :param bool block_move: Tile can be moved through
        :param bool block_sight: Tile can be seen through
        :param int hardness: Difficulty rating to carve through this tile
        """
        self.block_move = block_move

        if block_sight is None:
            self.block_sight = block_move
        else:
            self.block_sight = block_sight

        if block_move:
            self.hardness = hardness
        else:
            self.hardness = 0

        self.resources = []
        self.explored = False

    def clear(self):
        """
        Make this tile an open space
        """
        self.hardness = 0
        self.block_move = False
        self.block_sight = False

    def dig(self, strength=1):
        """
        Carve through this tile
        :param strength: Speed at which digging occurs
        :return dict: Ore type and quantity
        """
        if self.hardness > strength:
            self.hardness -= strength
            return None
        else:
            self.clear()
            mined_resources = []
            for resource in self.resources:
                mined_resources.append(resource())
            self.resources = []
            return mined_resources
