import random

import pygame
from pygame.locals import *
import os
import sys
import math


def load(fn: str):
    return pygame.image.load(os.path.join('resources', fn))


pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = load('bg.png').convert()
bg_x = 0
bg_x2 = bg.get_width()

clock = pygame.time.Clock()


class Saw(object):
    rotate = [load(f'SAW{i}.png') for i in range(0, 4)]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotate_count = 0
        self.vel = 1.4
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        if self.rotate_count >= 8:
            self.rotate_count = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotate_count // 2], (64, 64)), (self.x, self.y))
        self. rotate_count += 1


class Spike(Saw):
    img = load('spike.png')

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))


class Player(object):
    run = [load(f'{x}.png') for x in range(8, 16)]
    jump = [load(f'{x}.png') for x in range(1, 8)]
    slide = [load(f'S{x}.png') for x in [1, 2, 2, 2, 2, 2, 2, 2, 3, 4, 5]]
    jump_list = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4,
                 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1,
                 -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                 -3, -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slide_count = 0
        self.jump_count = 0
        self.run_count = 0
        self.slide_up = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jump_list[self.jump_count] * 1.2
            win.blit(self.jump[self.jump_count // 18], (self.x, self.y))
            self.jump_count += 1
            if self.jump_count > 108:
                self.jump_count = 0
                self.jumping = False
                self.run_count = 0
        elif self.sliding or self.slide_up:
            if self.slide_count < 20:
                self.y += 1
            elif self.slide_count == 80:
                self.y -= 19
                self.sliding = False
                self.slide_up = True
            if self.slide_count >= 110:
                self.slide_count = 0
                self.slide_up = False
                self.run_count = 0
            win.blit(self.slide[self.slide_count // 10], (self.x, self.y))
            self.slide_count += 1
        else:
            if self.run_count > 42:
                self.run_count = 0
            win.blit(self.run[self.run_count // 6], (self.x, self.y))
            self.run_count += 1


def redraw_window():
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    pygame.display.update()


run = True
speed = 30
pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, random.randrange(2000, 3500))
runner = Player(200, 313, 64, 64)
obstacles = []

while run:
    redraw_window()

    for obstacle in obstacles:
        obstacle.x -= 1.4
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))

    bg_x -= 1.4
    bg_x2 -= 1.4

    if bg_x < bg.get_width() * -1:
        bg_x = bg.get_width()
    if bg_x2 < bg.get_width() * -1:
        bg_x2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT + 1:
            speed += 1
        if event.type == USEREVENT + 2:
            r = random.randrange(0, 2)
            if r == 0:
                obstacles.append(Saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(Spike(810, 0, 48, 310))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not runner.jumping:
            runner.jumping = True
    if keys[pygame.K_DOWN]:
        runner.sliding = True

    clock.tick(speed)
