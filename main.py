import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

resource_dir = "resources/"


def load(s):
    return pygame.image.load(f"{resource_dir}{s}")


walk_right = [load('R1.png'), load('R2.png'), load('R3.png'), load('R4.png'), load('R5.png'), load('R6.png'),
              load('R7.png'), load('R8.png'), load('R9.png')]
walk_left = [load('L1.png'), load('L2.png'), load('L3.png'), load('L4.png'), load('L5.png'), load('L6.png'),
             load('L7.png'), load('L8.png'), load('L9.png')]
bg = load('bg.jpg')
character = load('standing.png')

clock = pygame.time.Clock()


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self. vel = 8 * facing

    def draw(self, w):
        pygame.draw.circle(w, self.color, (self.x, self.y), self.radius)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10
        self.standing = True

    def draw(self, w):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                w.blit(walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                w.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                w.blit(walk_right[0], (self.x, self.y))
            else:
                w.blit(walk_left[0], (self.x, self.y))


def redraw_game_window():
    win.blit(bg, (0, 0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = Player(200, 410, 64, 64)
run = True

bullets = []

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width // 2),
                                      round(man.y + man.height // 2),
                                      6,
                                      (0, 0, 0),
                                      facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 500 - man.vel - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walk_count = 0

    if not man.is_jump:
        if keys[pygame.K_UP]:
            man.is_jump = True
            man.left = False
            man.right = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10

    redraw_game_window()

pygame.quit()
