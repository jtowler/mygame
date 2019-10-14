import pygame
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
x = bg_x2 / 2
y = bg_y2 / 2

print(bg_x2, bg_y2)

run = True
while run:

    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 5
    elif keys[pygame.K_RIGHT]:
        x += 5
    elif keys[pygame.K_UP]:
        y -= 5
    elif keys[pygame.K_DOWN]:
        y += 5

    win.fill((0, 0, 0))
    win.blit(bg, (x - width / 2, y - height / 2))
    pygame.display.update()
