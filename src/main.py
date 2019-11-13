import random

import pygame
import math
import os

from player import Player
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
    # x = bg_x // 2
    # y = bg_y // 2

    player = Player(bg_x // 2, bg_y // 2)

    enemies = [Enemy(random.randrange(0, width), random.randrange(0, height), 10)]

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
        player.move(bg_x, bg_y)
        # keys = pygame.key.get_pressed()
        #
        # hori = 0
        # vert = 0
        # if keys[pygame.K_a] and x > 0:
        #     hori -= 5
        # if keys[pygame.K_d] and x < bg_x:
        #     hori += 5
        # if keys[pygame.K_w] and y > 0:
        #     vert -= 5
        # if keys[pygame.K_s] and y < bg_y:
        #     vert += 5
        #
        # if hori and vert:
        #     hori = int(hori / math.sqrt(2))
        #     vert = int(vert / math.sqrt(2))
        #
        # x += hori
        # y += vert

        mouse_x, mouse_y = pygame.mouse.get_pos()
        r_x, r_y = project(mouse_x, mouse_y, width, height, 20)
        rw = r_x + w2
        rh = r_y + h2
        theta = get_angle(mouse_x, mouse_y, width, height)

        if projectile_tick == 0:
            if pygame.mouse.get_pressed()[0]:
                projectiles.append(Projectile(player.x + r_x, player.y + r_y, theta, 1))
                projectile_tick = 1
        elif projectile_tick < projectile_cooldown:
            projectile_tick += 1
        else:
            projectile_tick = 0

        win.fill((0, 0, 0))
        win.blit(bg, (w2 - player.x, h2 - player.y))
        pygame.draw.circle(win, (255, 0, 0), (w2, h2), 10)
        pygame.draw.line(win, (255, 0, 0), (w2, h2), (rw, rh), 4)

        for projectile in projectiles:
            a_x = projectile.x - player.x
            a_y = projectile.y - player.y
            projectile.draw(win, w2 + a_x, h2 + a_y)
            projectile.move()
            if abs(a_x) > width or abs(a_y) > height:
                projectiles.remove(projectile)
            for enemy in enemies:
                if enemy.is_hit(projectile):
                    projectiles.remove(projectile)
                    enemy.hit()

        for enemy in enemies:
            if enemy.is_dead():
                enemies.remove(enemy)
            a_x = enemy.x - player.x
            a_y = enemy.y - player.y
            enemy.draw(win, w2 + a_x, h2 + a_y)
            enemy.move()

        pygame.display.update()


if __name__ == "__main__":
    main()
