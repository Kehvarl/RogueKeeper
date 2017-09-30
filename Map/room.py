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

    def get_center(self):
        """
        Get the center of the room
        :return int, int: x position, y position
        """
        x = self.x1 + int((self.x2 - self.x1) / 2)
        y = self.y1 + int((self.y2 - self.y1) / 2)
        return x, y

    def get_random_point(self):
        """
        Get a random point in the room
        :return int, int: x position, y position
        """
        x = randint(self.x1, self.x2)
        y = randint(self.y1, self.y2)
        return x, y

    def add_component(self, component=None):
        """
        Add a room component
        :param component:
        """
        if component:
            component.owner = self
            self.components.append(component)

    def remove_component(self, component=None):
        """
        Remove a component from the room
        :param component:
        :return:
        """
        if component and component in self.components:
            self.components.remove(component)
