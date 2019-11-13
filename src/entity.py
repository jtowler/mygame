import math
import random
import pygame

from player import Player
from utilities.geometry import get_projections


class Projectile(object):

    def __init__(self, x: int, y: int, theta: float, radius: int) -> None:
        self.x = x
        self.y = y
        self.theta = theta
        self.radius = radius
        self.v = 8

    def move(self) -> None:
        r_x, r_y = get_projections(self.v, self.theta)
        self.x += int(r_x)
        self.y += int(r_y)

    def draw(self, win, player: Player, mid_x, mid_y):
        a_x = self.x - player.x
        a_y = self.y - player.y
        pygame.draw.circle(win, (255, 255, 255), (mid_x + a_x, mid_y + a_y), self.radius)

    def is_offscreen(self, player: Player, width: int, height: int) -> bool:
        a_x = self.x - player.x
        a_y = self.y - player.y
        return abs(a_x) > width or abs(a_y) > height


class Enemy(object):

    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.theta = random.random() * math.pi * 2
        self.v = 3
        self.hits = 5

    def move(self) -> None:
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

    def is_hit(self, projectile: Projectile) -> bool:
        dist_sq = (self.x - projectile.x) * (self.x - projectile.x) + (self.y - projectile.y) * (self.y - projectile.y)
        rad_sum_sq = (self.radius + projectile.radius) * (self.radius + projectile.radius)
        return dist_sq < rad_sum_sq

    def hit(self) -> None:
        self.hits -= 1

    def is_dead(self) -> bool:
        return self.hits <= 0

    def draw(self, win, player: Player, mid_x: int, mid_y: int) -> None:
        a_x = self.x - player.x
        a_y = self.y - player.y
        pygame.draw.circle(win, (0, 255, 0), (mid_x + a_x, mid_y + a_y), self.radius)

    def is_offscreen(self, player: Player, width: int, height: int) -> bool:
        a_x = self.x - player.x
        a_y = self.y - player.y
        return abs(a_x) > width or abs(a_y) > height
