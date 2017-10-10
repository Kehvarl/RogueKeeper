from Map.tile import Tile


class Line:
    """
    Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
    """
    def __init__(self, x0, y0, x1, y1):
        self.points = []
        self.calculate_line(x0, y0, x1, y1)

    def calculate_line(self, x0, y0, x1, y1):
        # Initial conditions
        dx = x1 - x0
        dy = y1 - y0

        # Determine line steepness
        is_steep = abs(dy) > abs(dx)

        # Rotate the line if it's too steep
        if is_steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Swap start and end points if necessary.
        swapped = False
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            swapped = True

        # Recalculate differential
        dx = x1 - x0
        dy = y1 - y0

        # Calculate Error
        error = int(dx / 2.0)
        y_step = 1 if y0 < y1 else -1

        # Iterate over bounding box and generate points between start and end
        y = y1
        self.points = []
        for x in range(x0, x1 + 1):
            coord = (y, x) if is_steep else (x, y)
            self.points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += y_step
                error += dx

        # Reverse the list if the start and end were swapped
        if swapped:
            self.points.reverse()


class ViewTile:
    def __init__(self, visible=False):
        self.visible = visible


class FieldOfView:
    def __init__(self, game_map):
        self.game_map = game_map
        self.visible = [
            [ViewTile(False)
             for _ in range(game_map.height)]
            for _ in range(game_map.width)]
        self.tiles = [
            [Tile()
             for _ in range(game_map.height)]
            for _ in range(game_map.width)]

    def update(self, player_x, player_y, sight_radius=10):
        sight_range = sight_radius * sight_radius

        for y in range(-sight_radius, sight_radius):
            for x in range(-sight_radius, sight_radius):
                if x*x + y*y > sight_range:
                    continue

                if not (0 < player_y + y < self.game_map.height and
                        0 < player_x + x < self.game_map.width):
                    continue

                for point_x, point_y in Line(player_x, player_y, player_x+x, player_y + y).points:
                    self.tiles[point_x][point_y] = self.game_map.tiles[point_x][point_y]
                    self.visible[point_x][point_y].visible = True
