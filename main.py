import pygame

resource_dir = "resources/"


def load(s):
    return pygame.image.load(f"{resource_dir}{s}")


walk_right = [load('R1.png'), load('R2.png'), load('R3.png'), load('R4.png'), load('R5.png'), load('R6.png'),
              load('R7.png'), load('R8.png'), load('R9.png')]
walk_left = [load('L1.png'), load('L2.png'), load('L3.png'), load('L4.png'), load('L5.png'), load('L6.png'),
             load('L7.png'), load('L8.png'), load('L9.png')]
bg = load('bg.jpg')
character = load('standing.png')

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

x = 50
y = 400
width = 40
height = 60
vel = 5

clock = pygame.time.Clock()

is_jump = False
jump_count = 10

left = False
right = False
walk_count = 0


def redraw_game_window():
    global walk_count

    win.blit(bg, (0, 0))
    if walk_count + 1 >= 27:
        walk_count = 0

    if left:
        win.blit(walk_left[walk_count // 3], (x, y))
        walk_count += 1
    elif right:
        win.blit(walk_right[walk_count // 3], (x, y))
        walk_count += 1
    else:
        win.blit(character, (x, y))
        walk_count = 0

    pygame.display.update()


run = True

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT] and x < 500 - vel - width:
        x += vel
        left = False
        right = True

    else:
        left = False
        right = False
        walk_count = 0

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
            left = False
            right = False
            walk_count = 0
    else:
        if jump_count >= -10:
            y -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else:
            jump_count = 10
            is_jump = False

    redraw_game_window()

pygame.quit()
