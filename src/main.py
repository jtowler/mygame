import random

import pygame
import os

from entity import Player
from enemy import Minion, Tank, Runner

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

    font = pygame.font.SysFont('helvetica', 20)

    player = Player(bg_x // 2, bg_y // 2)

    enemies = [Minion(random.randrange(0, bg_x), random.randrange(0, bg_y)) for _ in range(10)] + \
              [Runner(random.randrange(0, bg_x), random.randrange(0, bg_y)) for _ in range(3)] + \
              [Tank(random.randrange(0, bg_x), random.randrange(0, bg_y))]

    projectiles = []
    projectile_tick = 0
    score = 0
    run = True

    while run:

        clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move(bg_x, bg_y, width, height)
        if projectile_tick == 0:
            if pygame.mouse.get_pressed()[0]:
                projectiles.extend(player.shoot(w2, h2))
                projectile_tick = 1
        elif projectile_tick < player.gun.cooldown:
            projectile_tick += 1
        else:
            projectile_tick = 0

        win.fill((0, 0, 0))
        win.blit(bg, (w2 - player.x, h2 - player.y))
        player.draw(win, player, w2, h2)

        for projectile in projectiles:
            projectile.draw(win, player, w2, h2)
            projectile.move()
            if projectile.is_offscreen(player, width, height):
                projectiles.remove(projectile)
            for enemy in enemies:
                if enemy.is_hit(projectile):
                    projectiles.remove(projectile)
                    enemy.hit(projectile)
                    if enemy.is_dead():
                        score += enemy.points
                        enemies.remove(enemy)
                    break

        for enemy in enemies:
            if not enemy.is_offscreen(player, width, height):
                enemy.move(bg_x, bg_y, player)
                enemy.draw(win, player, w2, h2)

        text = font.render(f'Score: {score}', True, (255, 255, 255))
        win.blit(text, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()
