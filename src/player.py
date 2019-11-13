import math
import pygame


class Player(object):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def move(self, max_x: int, max_y: int) -> None:
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

    def draw(self, win, mid_x, mid_y) -> None:
        pygame.draw.circle(win, (255, 0, 0), (mid_x, mid_y), 10)
