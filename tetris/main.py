import pygame
import random
from tetris.blocks import shapes, shape_colors, Piece

pygame.font.init()

s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, row, col):
    pass


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('helvetica', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.display.update()


def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
        draw_window(win)


def main_menu():
    pass


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

main()  # start game
