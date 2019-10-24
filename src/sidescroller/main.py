import random
import pygame
from pygame.locals import *
import os


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
        self.rotate_count += 1

    def collide(self, rect):
        return (rect[0] + rect[2] > self.hitbox[0] and
                rect[0] < self.hitbox[0] + self.hitbox[2] and
                rect[1] + rect[3] > self.hitbox[1])


class Spike(Saw):
    img = load('spike.png')

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        return (rect[0] + rect[2] > self.hitbox[0] and
                rect[0] < self.hitbox[0] + self.hitbox[2] and
                rect[1] < self.hitbox[3])


class Player(object):
    run = [load(f'{x}.png') for x in range(8, 16)]
    jump = [load(f'{x}.png') for x in range(1, 8)]
    slide = [load(f'S{x}.png') for x in [1, 2, 2, 2, 2, 2, 2, 2, 3, 4, 5]]
    fall = load('0.png')
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
        self.falling = False
        self.slide_count = 0
        self.jump_count = 0
        self.run_count = 0
        self.slide_up = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jump_list[self.jump_count] * 1.2
            win.blit(self.jump[self.jump_count // 18], (self.x, self.y))
            self.jump_count += 1
            if self.jump_count > 108:
                self.jump_count = 0
                self.jumping = False
                self.run_count = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slide_up:
            if self.slide_count < 20:
                self.y += 1
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            elif self.slide_count == 80:
                self.y -= 19
                self.sliding = False
                self.slide_up = True
            elif 20 < self.slide_count < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
            if self.slide_count >= 110:
                self.slide_count = 0
                self.slide_up = False
                self.run_count = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slide_count // 10], (self.x, self.y))
            self.slide_count += 1
        else:
            if self.run_count > 42:
                self.run_count = 0
            win.blit(self.run[self.run_count // 6], (self.x, self.y))
            self.run_count += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)


def update_file():
    f = open('scores.txt', 'r')
    file = f.readlines()
    last = int(file[0])
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
    return last


def redraw_window():
    large_font = pygame.font.SysFont('helvetica', 30)
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x2, 0))
    text = large_font.render(f'Score: {score}', 1, (255, 255, 255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    win.blit(text, (700, 10))
    pygame.display.update()


def end_screen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False
        win.blit(bg, (0, 0))
        large_font = pygame.font.SysFont('helvetica', 80)
        last_score = large_font.render(f'Best Score: {update_file()}', 1, (255, 255, 255))
        current_score = large_font.render(f'Score: {score}', 1, (255, 255, 255))
        win.blit(last_score, (W / 2 - last_score.get_width() / 2, 150))
        win.blit(current_score, (W / 2 - current_score.get_width() / 2, 240))
        pygame.display.update()
    score = 0


run = True
speed = 30
fall_speed = 0
pause = 0
pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, 3000)
runner = Player(200, 313, 64, 64)
obstacles = []
score = 0

while run:
    redraw_window()

    score = speed // 5 - 6

    if pause > 0:
        pause += 1
    if pause > fall_speed * 2:
        end_screen()

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True
            if pause == 0:
                fall_speed = speed
                pause = 1
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
