import pygame
import math
import os

pygame.init()


def load(fn: str):
    return pygame.image.load(os.path.join('resources', fn))


width = 300
height = 300


clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('MyGame')


bg = load('test_bg.png').convert()
bg_x = 0
bg_y = 0
bg_x2 = bg.get_width()
bg_y2 = bg.get_height()
x = bg_x2 // 2
y = bg_y2 // 2

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
    if keys[pygame.K_LEFT] and x > 0:
        hori -= 5
    if keys[pygame.K_RIGHT] and x < bg_x2:
        hori += 5
    if keys[pygame.K_UP] and y > 0:
        vert -= 5
    if keys[pygame.K_DOWN] and y < bg_y2:
        vert += 5

    if hori and vert:
        hori = hori / math.sqrt(2)
        vert = vert / math.sqrt(3)

    x += hori
    y += vert

    win.fill((0, 0, 0))
    win.blit(bg, (width / 2 - x, height / 2 - y))
    pygame.draw.circle(win, (255, 0, 0), (width // 2, height // 2), 10)
    pygame.display.update()
