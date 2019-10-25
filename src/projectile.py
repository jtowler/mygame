from utilities.geometry import get_projections


class Projectile(object):

    def __init__(self, x: int, y: int, theta: float):
        self.x = x
        self.y = y
        self.theta = theta
        self.v = 5

    def move(self):
        r_x, r_y = get_projections(self.v, self.theta)
        self.x += int(r_x)
        self.y += int(r_y)

    def draw(self, win):
        pass