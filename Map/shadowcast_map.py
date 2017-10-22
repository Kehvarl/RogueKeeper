class ShadowcastMap:
    """
    Python Shadowcasting implementation
    Source: http://www.roguebasin.com/index.php?title=Python_shadowcasting_implementation
    """
    # Multipliers for transforming coordinates to other octant:
    mult_xx = [1,  0,  0, -1, -1,  0,  0,  1]
    mult_xy = [0,  1, -1,  0,  0, -1,  1,  0]
    mult_yx = [0,  1,  1,  0,  0, -1, -1,  0]
    mult_yy = [1,  0,  0,  1, -1,  0,  0, -1]

    def __init__(self, game_map):
        """
        Create FOV Map
        :param Map.game_map.GameMap game_map: Current level map
        """
        self.game_map = game_map
        self.in_fov = self._clear_fov()

    def recalculate_fov(self, x, y, radius):
        """
        Calculate the visible portion of the map for an entity
        :param int x: X coordinate of Entity
        :param int y: Y coordinate of Entity
        :param int radius: Distance Entity can see
        """
        self.in_fov = self._clear_fov()
        self.in_fov[x][y] = True
        for octant in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             ShadowcastMap.mult_xx[octant], ShadowcastMap.mult_xy[octant],
                             ShadowcastMap.mult_yx[octant], ShadowcastMap.mult_yy[octant])

    def is_in_fov(self, x, y):
        """
        Check if a given Tile is visible
        :param int x: Tile Coordinate
        :param int y: Tile Coordinate
        :return boolean: True if Tile can be seen.
        """
        return self.in_fov[x][y]

    def _clear_fov(self):
        """
        Reset the map visibility (All False)
        """
        return [
            [False
             for _ in range(self.game_map.height)]
            for _ in range(self.game_map.width)]

    def _cast_light(self,
                    cx, cy, row, start, end, radius,
                    xx, xy, yx, yy):
        """
        Recursive light-casting function
        :param int cx: entity_x coordinate
        :param int cy: entity_y coordinate
        :param int row:
        :param float start:
        :param float end:
        :param int radius: Distance of view
        :param int xx: octant transform parameter
        :param int xy: octant transform parameter
        :param int yx: octant transform parameter
        :param int yy: octant transform parameter
        """
        if start < end:
            return
        radius_squared = radius * radius
        for j in range(row, radius + 1):
            dx, dy = -j - 1, -j
            blocked = False
            new_start = start
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                x, y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.in_fov[x][y] = True
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.game_map.tiles[x][y].block_sight:
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.game_map.tiles[x][y].block_sight and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break
