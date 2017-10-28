from UI.render_functions import RenderOrder


class Entity:
    """
    Any object on the map
    """

    def __init__(self, x, y, char, color, name, blocks=False, treasure=None, resource=None,
                 render_order=RenderOrder.CORPSE):
        """
        Create an Entity
        :param int x: Location
        :param int y: Location
        :param string char:
        :param color: Display Color
        :param string name: Entity Name
        :param bool blocks: Blocks Movement through square
        :param bool treasure: carried treasure
        :param dict resource: carried resources
        :param RenderOrder render_order: Sets screen drawing sequence
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.treasure = treasure
        self.resource = resource
        self.components = {}
        self.render_order = render_order

    def move(self, dx, dy):
        """
        Adjust entity location
        :param int dx: Change in position
        :param int dy: Change in position
        """
        self.x += dx
        self.y += dy

    def add_component(self, component):
        """
        Add a feature to this entity
        :param component:
        """
        self.components[component.label] = component
