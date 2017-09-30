class Tile:
    """
    A tile on the map
    """
    def __init__(self, block_move=True, block_sight=None):
        """
        Create a new Tile
        :param bool block_move: Tile can be moved through
        :param bool block_sight: Tile can be seen through
        """
        self.block_move = block_move
        if block_sight is None:
            self.block_sight = block_move
        else:
            self.block_sight = block_sight