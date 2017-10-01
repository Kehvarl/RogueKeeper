from random import randint


class Room:
    """
    A room in the Game Map
    """
    def __init__(self, x, y, w, h):
        """
        Create a new Room in the current Game Map
        :param int x: Top of room
        :param int y: Left of room
        :param int w: Size of room
        :param int h: Size of room
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.components = []

    def intersect(self, other):
        """
        Check for overlapping rooms
        :param Room other: other room to test
        :return bool: True if the two rooms overlap
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def center(self):
        """
        Get the center of the room
        :return int, int: x position, y position
        """
        x = int((self.x1 + self.x2) / 2)
        y = int((self.y1 + self.y2) / 2)
        return x, y

    def random_point(self):
        """
        Get a random point in the room
        :return int, int: x position, y position
        """
        x = randint(self.x1, self.x2)
        y = randint(self.y1, self.y2)
        return x, y
