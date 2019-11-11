import math
import random

from utilities.geometry import get_projections


class Projectile(object):

    def __init__(self, x: int, y: int, theta: float):
        self.x = x
        self.y = y
        self.theta = theta
        self.v = 8

    def move(self):
        r_x, r_y = get_projections(self.v, self.theta)
        self.x += int(r_x)
        self.y += int(r_y)


class Enemy(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.theta = random.random() * math.pi * 2
        self.v = 3

    def move(self):
        r = random.random()
        if r < 0.2:
            self.theta += 1
            if self.theta > 2 * math.pi:
                self.theta = 2 * math.pi - self.theta
        elif r > 0.8:
            self.theta -= 1
            if self.theta < 0:
                self.theta = self.theta + 2 * math.pi

        r_x, r_y = get_projections(self.v, self.theta)
        self.x += int(r_x)
        self.y += int(r_y)
