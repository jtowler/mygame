import random
import pygame

from utilities.geometry import *


class Player(object):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.gun = Gun()

    def move(self, max_x: int, max_y: int, width: int, height: int) -> None:
        keys = pygame.key.get_pressed()

        hori = 0
        vert = 0
        if keys[pygame.K_a] and self.x > 0:
            hori -= 5
        if keys[pygame.K_d] and self.x < max_x:
            hori += 5
        if keys[pygame.K_w] and self.y > 0:
            vert -= 5
        if keys[pygame.K_s] and self.y < max_y:
            vert += 5

        if hori and vert:
            hori = int(hori / math.sqrt(2))
            vert = int(vert / math.sqrt(2))

        self.x += hori
        self.y += vert

        self.gun.update_position(width, height)

    def draw(self, win, mid_x, mid_y) -> None:
        pygame.draw.circle(win, (255, 0, 0), (mid_x, mid_y), 10)
        self.gun.draw(win, mid_x, mid_y)

    def shoot(self, w2: int, h2: int):
        return Projectile(self.x + self.gun.x - w2, self.y + self.gun.y - h2, self.gun.theta, 1)


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


class Gun(object):

    def __init__(self, x: int = 0, y: int = 0, theta: float = 0.) -> None:
        self.x = x
        self.y = y
        self.theta = theta

    def update_position(self, width: int, height: int) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        r_x, r_y = project(mouse_x, mouse_y, width, height, 20)
        self.x = r_x + width // 2
        self.y = r_y + height // 2
        self.theta = get_angle(mouse_x, mouse_y, width, height)

    def shoot(self) -> None:
        pass

    def draw(self, win, mid_x: int, mid_y: int) -> None:
        pygame.draw.line(win, (255, 0, 0), (mid_x, mid_y), (self.x, self.y), 4)
