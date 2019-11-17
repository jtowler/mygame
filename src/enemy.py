import random
import math
from typing import Tuple

from utilities.geometry import get_projections

from entity import Entity, Projectile, Player


class Enemy(Entity):

    def __init__(self, x: int, y: int, radius: int, colour: Tuple[int, int, int], v: float, hits: float,
                 points: float) -> None:
        super().__init__(x, y, radius, (0, 255, 0))
        self.theta = random.random() * math.pi * 2
        self.v = v
        self.hits = hits
        self.colour = colour
        self.points = points

    def hit(self, projectile: Projectile) -> None:
        self.hits -= projectile.damage

    def is_dead(self) -> bool:
        return self.hits <= 0


class Minion(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 10, (0, 255, 0), 4, 5, 1)
        self.theta = random.random() * math.pi * 2

    def move(self, max_x, max_y, player: Player) -> None:
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
        if 0 < self.x + int(r_x) < max_x:
            self.x += int(r_x)
        if 0 < self.y + int(r_y) < max_y:
            self.y += int(r_y)


class Tank(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 10, (0, 0, 255), 3, 15, 5)

    def move(self, max_x: int, max_y: int, player: Player) -> None:

        theta = math.atan2(self.y - player.y, self.x - player.x)
        r_x, r_y = get_projections(self.v, theta)
        if 0 < self.x + int(r_x) < max_x:
            self.x -= int(r_x)
        if 0 < self.y + int(r_y) < max_y:
            self.y -= int(r_y)


class Runner(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 10, (0, 255, 255), 5, 3, 2)

    def move(self, max_x: int, max_y: int, player: Player) -> None:

        theta = math.atan2(self.y - player.y, self.x - player.x)
        r_x, r_y = get_projections(self.v, theta)
        if 0 < self.x + int(r_x) < max_x:
            self.x += int(r_x)
        if 0 < self.y + int(r_y) < max_y:
            self.y += int(r_y)
