from ..utils.vector import Vector2


class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        x_s_max = self.screen_size[0]
        y_s_max = self.screen_size[1]
        scale = self.scale
        x_w = position.get_x()
        y_w = position.get_y()
        x_c = self.position.get_x()
        y_c = self.position.get_y()
        x_s = x_s_max/2+(x_w-x_c)*scale
        y_s = y_s_max/2+(y_w-y_c)*scale
        return Vector2(int(x_s),int(y_s))

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        x_s = position.get_x()
        y_s = position.get_y()
        x_s_max = self.screen_size[0]
        y_s_max = self.screen_size[1]
        scale = self.scale
        x_c = self.position.get_x()
        y_c = self.position.get_y()
        x_w = (x_s-x_s_max/2)/scale + x_c
        y_w = (y_s-y_s_max/2)/scale + y_c
        return Vector2(x_w, y_w)
