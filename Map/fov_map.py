from Map.tile import Tile


class Line:
    """
    Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
    """
    def __init__(self, x0, y0, x1, y1):
        self.points = self.get_points(x0, y0, x1, y1)

    @staticmethod
    def get_points(x0, y0, x1, y1):
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
        points = []
        for x in range(x0, x1 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += y_step
                error += dx

        # Reverse the list if the start and end were swapped
        if swapped:
            points.reverse()

        return points


class FieldOfView:
    def __init__(self, game_map):
        self.game_map = game_map
        self.visible = self.initialize_view()
        self.tiles = [
            [Tile()
             for _ in range(game_map.height)]
            for _ in range(game_map.width)]

    def initialize_view(self):
        visible = [
            [False
             for _ in range(self.game_map.height)]
            for _ in range(self.game_map.width)]
        return visible

    def update(self, player_x, player_y, sight_radius=10):
        self.visible = self.initialize_view()
        sight_range = sight_radius * sight_radius
        for y in range(-sight_radius, sight_radius):
            for x in range(-sight_radius, sight_radius):
                if x * x + y * y > sight_range:
                    continue
                if not self.game_map.point_in_map(player_x + x, player_y + y):
                    continue

                points = Line.get_points(player_x, player_y, player_x + x, player_y + y)
                print(points)
                for point in points:
                    if self.game_map.point_in_map(point[0], point[1]):
                        self.tiles[point[0]][point[1]] = self.game_map.tiles[point[0]][point[1]]
                        self.visible[point[0]][point[1]] = True
