'''
Created on Sep 16, 2021
@author joeypy
'''

import os
import sys
import cfg
import random
import pygame


# Check if game is over
def is_game_over(board, size):
    assert isinstance(size, int)
    num_cells = size * size
    for i in range(num_cells - 1):
        if board[i] != i:
            return False
    return True


# Move the piece to right
def move_right(board, blank_cell_idx, num_cols):
    if blank_cell_idx % num_cols == 0:
        return blank_cell_idx
    board[blank_cell_idx - 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - 1]
    return blank_cell_idx - 1


# Move the piece to left
def move_left(board, blank_cell_idx, num_cols):
    if (blank_cell_idx + 1) % num_cols == 0:
        return blank_cell_idx
    board[blank_cell_idx + 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + 1]
    return blank_cell_idx + 1


# Move the piece to down
def move_down(board, blank_cell_idx, num_cols):
    if blank_cell_idx < num_cols:
        return blank_cell_idx
    board[blank_cell_idx - num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - num_cols]
    return blank_cell_idx - num_cols


# Move the piece to up
def move_up(board, blank_cell_idx, num_rows, num_cols):
    if blank_cell_idx >= (num_rows - 1) * num_cols:
        return blank_cell_idx
    board[blank_cell_idx + num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + num_cols]
    return blank_cell_idx + num_cols


# Create the board game
def create_board(num_rows, num_cols, num_cells):
    board = []

    for i in range(num_cells):
        board.append(i)

    blank_cell_idx = num_cells - 1
    board[blank_cell_idx] = -1

    for i in range(cfg.RANDOM_NUM):
        direction = random.randint(0, 3)
        if direction == 0:
            blank_cell_idx = move_left(board, blank_cell_idx, num_cols)
        elif direction == 1:
            blank_cell_idx = move_right(board, blank_cell_idx, num_cols)
        elif direction == 2:
            blank_cell_idx = move_up(board, blank_cell_idx, num_rows, num_cols)
        elif direction == 3:
            blank_cell_idx = move_down(board, blank_cell_idx, num_cols)
    return board, blank_cell_idx


# Read the image files
def get_image_paths(root_dir):
    image_names = os.listdir(root_dir)
    assert len(image_names) > 0
    return os.path.join(root_dir, random.choice(image_names))


# Show end interface of the game
def show_end_interface(screen, width, height):
    screen.fill(cfg.BACKGROUND_COLOR)
    font = pygame.font.Font(cfg.FONT_PATH, width // 15)
    title = font.render('Good Job! You Won!', True, (233, 150, 122))
    rectangle = title.get_rect()
    rectangle.midtop = (width / 2, height / 2)
    screen.blit(title, rectangle)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()
        pygame.display.update()


# Show the start menu interface
def show_start_interface(screen, width, height):
    screen.fill(cfg.BACKGROUND_COLOR)
    t_font = pygame.font.Font(cfg.FONT_PATH, width // 4)
    c_font = pygame.font.Font(cfg.FONT_PATH, width // 22)
    title = t_font.render('Puzzle', True, cfg.RED)
    content_1 = c_font.render("Press H, M or L to choose your puzzle", True, cfg.BLUE)
    content_2 = c_font.render("H- 5x5, M- 4x4, L- 3x3 to choose your puzzle", True, cfg.BLUE)
    # rectangle
    t_rectangle = title.get_rect()
    t_rectangle.midtop = (width / 2, height / 10)
    # rectangle 1
    c_rectangle_1 = content_1.get_rect()
    c_rectangle_1.midtop = (width / 2, height / 2.2)
    # rectangle 2
    c_rectangle_2 = content_2.get_rect()
    c_rectangle_2.midtop = (width / 2, height / 1.8)
    screen.blit(title, t_rectangle)
    screen.blit(content_1, c_rectangle_1)
    screen.blit(content_2, c_rectangle_2)
    # Check the play mode: 3x3, 4x4, 5x5
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('l'):
                    return 3
                elif event.key == ord('m'):
                    return 4
                elif event.key == ord('h'):
                    return 5
        pygame.display.update()


# Main game function
def main():
    pygame.init()
    clock = pygame.time.Clock()

    game_img_used = pygame.image.load(get_image_paths(cfg.PICTURE_ROOT_DIR))
    game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
    game_img_used_rectangle = game_img_used.get_rect()

    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Pokemon')

    size = show_start_interface(screen, game_img_used_rectangle.width, game_img_used_rectangle.height)
    assert isinstance(size, int)
    num_rows, num_cols = size, size
    num_cells = size * size

    cell_width = game_img_used_rectangle.width // num_cols
    cell_height = game_img_used_rectangle.height // num_rows

    while True:
        game_board, blank_cell_idx = create_board(num_rows, num_cols, num_cells)
        if not is_game_over(game_board, size):
            break
    is_running = True

    # The game logic
    while is_running:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Check events from the arrows keyboard or letters
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    blank_cell_idx = move_left(game_board, blank_cell_idx, num_cols)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    blank_cell_idx = move_right(game_board, blank_cell_idx, num_cols)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    blank_cell_idx = move_up(game_board, blank_cell_idx, num_rows, num_cols)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    blank_cell_idx = move_down(game_board, blank_cell_idx, num_cols)

            # Check events from the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_position = x // cell_width
                y_position = y // cell_height
                idx = x_position + y_position * num_cols
                if idx == blank_cell_idx - 1:
                    blank_cell_idx = move_right(game_board, blank_cell_idx, num_cols)
                elif idx == blank_cell_idx + 1:
                    blank_cell_idx = move_left(game_board, blank_cell_idx, num_cols)
                elif idx == blank_cell_idx + num_cols:
                    blank_cell_idx = move_up(game_board, blank_cell_idx, num_rows, num_cols)
                elif idx == blank_cell_idx - num_cols:
                    blank_cell_idx = move_down(game_board, blank_cell_idx, num_cols)

        # Check if game finished
        if is_game_over(game_board, size):
            game_board[blank_cell_idx] = num_cells - 1
            is_running = False

        screen.fill(cfg.BACKGROUND_COLOR)
        for i in range(num_cells):
            if game_board[i] == -1:
                continue
            x_position = i // num_cols
            y_position = i % num_cols
            rectangle = pygame.Rect(
                y_position * cell_width,
                x_position * cell_height,
                cell_width,
                cell_height
            )
            img_area = pygame.Rect(
                (game_board[i] % num_cols) * cell_width,
                (game_board[i] // num_cols) * cell_height,
                cell_width,
                cell_height
            )
            screen.blit(game_img_used, rectangle, img_area)

        for i in range(num_cols + 1):
            pygame.draw.line(
                screen,
                cfg.BLACK,
                (i * cell_width, 0),
                (i * cell_width, game_img_used_rectangle.height)
            )
        for i in range(num_rows + 1):
            pygame.draw.line(
                screen,
                cfg.BLACK,
                (0, i * cell_height),
                (game_img_used_rectangle.width, i * cell_height)
            )
        pygame.display.update()
        clock.tick(cfg.FPS)

    show_end_interface(screen, game_img_used_rectangle.width, game_img_used_rectangle.height)


if __name__ == '__main__':
    main()

