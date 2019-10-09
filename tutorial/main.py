import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

resource_dir = "tutorial/resources/"


def load(s):
    return pygame.image.load(f"{resource_dir}{s}")


bg = load('bg.jpg')
character = load('standing.png')

clock = pygame.time.Clock()
font = pygame.font.SysFont("helvetica", 30)

bullet_sound = pygame.mixer.Sound(f"{resource_dir}bullet.ogg")
hit_sound = pygame.mixer.Sound(f"{resource_dir}hit.ogg")

music = pygame.mixer.music.load(f"{resource_dir}music.mp3")
pygame.mixer.music.play(-1)


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, w):
        pygame.draw.circle(w, self.color, (self.x, self.y), self.radius)


class Entity(object):
    def __init__(self, x: int, y: int, width: int, height: int, vel: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.walk_count = 0


class Player(Entity):
    walk_right = [load(f'R{i}.png') for i in range(1, 10)]
    walk_left = [load(f'L{i}.png') for i in range(1, 10)]

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height, 5)
        self.is_jump = False
        self.left = False
        self.right = False
        self.jump_count = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, w):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                w.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                w.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                w.blit(self.walk_right[0], (self.x, self.y))
            else:
                w.blit(self.walk_left[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        self.x = 60
        self.y = 410
        self.walk_count = 0
        font1 = pygame.font.SysFont('helvetica', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    def is_hit(self, enemy: 'Enemy') -> bool:
        return (enemy.visible and
                self.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and
                self.hitbox[1] + self.hitbox[3] > enemy.hitbox[1] and
                self.hitbox[0] + self.hitbox[2] > enemy.hitbox[0] and
                self.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2])


class Enemy(Entity):
    walk_right = [load(f'R{i}E.png') for i in range(1, 12)]
    walk_left = [load(f'L{i}E.png') for i in range(1, 12)]

    def __init__(self, x: int, y: int, width: int, height: int, end: int) -> None:
        super().__init__(x, y, width, height, 3)
        self.path = [x, end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, w):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0
            if self.vel > 0:
                w.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
            else:
                w.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
            pygame.draw.rect(w, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(w, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walk_count = 0

    def hit(self):
        hit_sound.play()
        if self.health:
            self.health -= 1
        else:
            self.visible = False

    def is_hit(self, bullet: 'Projectile') -> bool:
        return (self.visible and
                bullet.y - bullet.radius < self.hitbox[1] + self.hitbox[3] and
                bullet.y + bullet.radius > self.hitbox[1] and
                bullet.x + bullet.radius > self.hitbox[0] and
                bullet.x - bullet.radius < self.hitbox[0] + self.hitbox[2])


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render(f"Score: {score}", 1, (0, 0, 0))
    win.blit(text, (10, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = Player(200, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 300)
run = True
shoot_loop = 0
score = 0
bullets = []

while run:
    clock.tick(27)

    if man.is_hit(goblin):
        man.hit()
        score -= 5

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.is_hit(bullet):
            goblin.hit()
            score += 1
            bullets.pop(bullets.index(bullet))

        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        bullet_sound.play()
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
