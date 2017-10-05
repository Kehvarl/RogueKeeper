class Entity:
    """
    Any object on the map
    """

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.components = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def add_component(self, component):
        self.components.append(component)
