import random
import pygame
from typing import Tuple, List

from utilities.geometry import *


class Entity(object):
    def __init__(self, x: int, y: int, radius: int, colour: Tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour

    def draw(self, win, that: 'Entity', mid_x: int, mid_y: int) -> None:
        a_x = self.x - that.x
        a_y = self.y - that.y
        pygame.draw.circle(win, self.colour, (mid_x + a_x, mid_y + a_y), self.radius)

    def is_offscreen(self, entity: 'Entity', width: int, height: int) -> bool:
        a_x = self.x - entity.x
        a_y = self.y - entity.y
        return abs(a_x) > width or abs(a_y) > height

    def is_hit(self, that: 'Entity') -> bool:
        dist_sq = (self.x - that.x) * (self.x - that.x) + (self.y - that.y) * (self.y - that.y)
        rad_sum_sq = (self.radius + that.radius) * (self.radius + that.radius)
        return dist_sq < rad_sum_sq


class Player(Entity):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 10, (255, 0, 0))
        self.v = 6
        self.gun = Pistol()
        self.max_health = 10
        self.curr_health = 10

    def move(self, max_x: int, max_y: int, width: int, height: int) -> None:
        keys = pygame.key.get_pressed()

        hori = 0
        vert = 0
        if keys[pygame.K_a] and self.x > 0:
            hori -= self.v
        if keys[pygame.K_d] and self.x < max_x:
            hori += self.v
        if keys[pygame.K_w] and self.y > 0:
            vert -= self.v
        if keys[pygame.K_s] and self.y < max_y:
            vert += self.v
        if keys[pygame.K_1]:
            self.gun = Pistol()
        if keys[pygame.K_2]:
            self.gun = Shotgun()
        if keys[pygame.K_3]:
            self.gun = Uzi()
        if keys[pygame.K_4]:
            self.gun = Bazooka()

        if hori and vert:
            hori = int(hori / math.sqrt(2))
            vert = int(vert / math.sqrt(2))

        self.x += hori
        self.y += vert

        self.gun.update_position(width, height)

    def draw(self, win, this, mid_x, mid_y) -> None:
        super().draw(win, this, mid_x, mid_y)
        self.gun.draw(win, this, mid_x, mid_y)

    def shoot(self, w2: int, h2: int) -> List['Projectile']:
        return self.gun.shoot(self.x, self.y, w2, h2)


class Projectile(Entity):

    def __init__(self, x: int, y: int, theta: float, radius: int, v: int, damage: int) -> None:
        super().__init__(x, y, radius, (255, 255, 255))
        self.theta = theta
        self.v = v
        self.damage = damage

    def move(self) -> None:
        r_x, r_y = get_projections(self.v, self.theta)
        self.x += int(r_x)
        self.y += int(r_y)


class Gun(Entity):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0., cooldown: int = 5, length: int = 20,
                 width: int = 4, proj_width: int = 1, proj_v: int = 8, proj_damage: int = 1) -> None:
        super().__init__(x, y, 4, (255, 0, 0))
        self.theta = theta
        self.cooldown = cooldown
        self.length = length
        self.width = width
        self.proj_width = proj_width
        self.proj_v = proj_v
        self.proj_damage = proj_damage

    def update_position(self, width: int, height: int) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        r_x, r_y = project(mouse_x, mouse_y, width, height, self.length)
        self.x = r_x + width // 2
        self.y = r_y + height // 2
        self.theta = get_angle(mouse_x, mouse_y, width, height)

    def draw(self, win, that: Entity, mid_x: int, mid_y: int) -> None:
        pygame.draw.line(win, self.colour, (mid_x, mid_y), (self.x, self.y), self.width)

    def shoot(self, x: int, y: int, w2: int, h2: int) -> List[Projectile]:
        return [
            Projectile(self.x + x - w2, self.y + y - h2, self.theta, self.proj_width, self.proj_v, self.proj_damage)
        ]


class Pistol(Gun):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0.) -> None:
        super().__init__(x, y, theta)


class Shotgun(Gun):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0.) -> None:
        self.pellets = 6
        super().__init__(x, y, theta, length=22, width=8, cooldown=10)

    def shoot(self, x: int, y: int, w2: int, h2: int) -> List[Projectile]:
        projectiles = []
        for _ in range(self.pellets):
            angle = self.theta + random.random() * 0.4 - 0.2
            projectiles.append(
                Projectile(self.x + x - w2, self.y + y - h2, angle, self.proj_width, self.proj_v, self.proj_damage)
            )
        return projectiles


class Uzi(Gun):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0.) -> None:
        super().__init__(x, y, theta, length=15, width=6, cooldown=3)


class Bazooka(Gun):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0.) -> None:
        super().__init__(x, y, theta, 20, 30, 8, 4, 6, 5)
