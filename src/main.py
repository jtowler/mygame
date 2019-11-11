import random

import pygame
import math
import os
from utilities.geometry import get_angle, project
from entity import Projectile, Enemy

pygame.init()


def load(fn: str):
    return pygame.image.load(os.path.join('resources', fn))


width = 300
height = 300
w2 = width // 2
h2 = height // 2

clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('MyGame')


bg = load('test_bg.png').convert()


def main():
    bg_x = bg.get_width()
    bg_y = bg.get_height()
    x = bg_x // 2
    y = bg_y // 2

    enemies = [Enemy(random.randrange(0, width), random.randrange(0, height))]

    projectiles = []
    projectile_tick = 0
    projectile_cooldown = 5
    run = True

    while run:

        clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()

        hori = 0
        vert = 0
        if keys[pygame.K_a] and x > 0:
            hori -= 5
        if keys[pygame.K_d] and x < bg_x:
            hori += 5
        if keys[pygame.K_w] and y > 0:
            vert -= 5
        if keys[pygame.K_s] and y < bg_y:
            vert += 5

        if hori and vert:
            hori = int(hori / math.sqrt(2))
            vert = int(vert / math.sqrt(2))

        x += hori
        y += vert

        mouse_x, mouse_y = pygame.mouse.get_pos()
        r_x, r_y = project(mouse_x, mouse_y, width, height, 20)
        rw = r_x + w2
        rh = r_y + h2
        theta = get_angle(mouse_x, mouse_y, width, height)

        if projectile_tick == 0:
            if pygame.mouse.get_pressed()[0]:
                projectiles.append(Projectile(x + r_x, y + r_y, theta))
                projectile_tick = 1
        elif projectile_tick < projectile_cooldown:
            projectile_tick += 1
        else:
            projectile_tick = 0

        win.fill((0, 0, 0))
        win.blit(bg, (w2 - x, h2 - y))
        pygame.draw.circle(win, (255, 0, 0), (w2, h2), 10)
        pygame.draw.line(win, (255, 0, 0), (w2, h2), (rw, rh), 4)

        for projectile in projectiles:
            a_x = projectile.x - x
            a_y = projectile.y - y
            pygame.draw.circle(win, (255, 255, 255), (w2 + a_x, h2 + a_y), 1)
            projectile.move()
            if abs(a_x) > width or abs(a_y) > height:
                projectiles.remove(projectile)

        for enemy in enemies:
            a_x = enemy.x - x
            a_y = enemy.y - y
            pygame.draw.circle(win, (0, 255, 0), (w2 + a_x, h2 + a_y), 10)
            enemy.move()

        pygame.display.update()


if __name__ == "__main__":
    main()
