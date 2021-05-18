from ..utils.vector import Vector2


class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        res = 1/2*self.screen_size + (position-self.position)*self.scale
        return Vector2(int(res.get_x()),int(res.get_y()))

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return (position-1/2*self.screen_size)/self.scale + self.position
