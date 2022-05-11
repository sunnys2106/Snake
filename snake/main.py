import pygame
import sys
import random

pygame.init()

WIN_SIDE_LENGTH = 600
ROWS = 15
WIN = pygame.display.set_mode((WIN_SIDE_LENGTH, WIN_SIDE_LENGTH))
CELL_SIZE = WIN_SIDE_LENGTH // ROWS

FPS = 60
SNAKE_MOVE = pygame.USEREVENT
SNAKE_MOVE_SPEED = 200
pygame.time.set_timer(SNAKE_MOVE, SNAKE_MOVE_SPEED)

WINNING_FONT = pygame.font.SysFont('comicsans', 100)
SMALL_WINNING_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('comicsans', 25)


def draw_fruit():
    global fruit_pos
    generate_new_food = True
    while(generate_new_food):
        if fruit_pos == []:
            fruit_pos = [random.randint(0, ROWS-1), random.randint(0, ROWS-1)]
            if fruit_pos in snake:
                fruit_pos = []
            else:
                generate_new_food = False
        else:
            generate_new_food = False
    fruit_rect = pygame.Rect(fruit_pos[0] * CELL_SIZE, fruit_pos[1] *
                             CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(WIN, (255, 0, 0), fruit_rect)


def draw_snake():
    for block in snake:
        block_rect = pygame.Rect(
            block[0]*CELL_SIZE, block[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(WIN, (0, 255, 0), block_rect)


def move_snake():
    global before_tail_cell
    if direction == 'UP':
        snake.insert(0, [snake[0][0], snake[0][1]-1])
        before_tail_cell = snake[-1]
        del snake[-1]
        check_for_food(snake[0])
        check_for_collision(snake[0])
    if direction == 'DOWN':
        snake.insert(0, [snake[0][0], snake[0][1]+1])
        before_tail_cell = snake[-1]
        del snake[-1]
        check_for_food(snake[0])
        check_for_collision(snake[0])
    if direction == 'RIGHT':
        snake.insert(0, [snake[0][0]+1, snake[0][1]])
        before_tail_cell = snake[-1]
        del snake[-1]
        check_for_food(snake[0])
        check_for_collision(snake[0])
    if direction == 'LEFT':
        snake.insert(0, [snake[0][0]-1, snake[0][1]])
        before_tail_cell = snake[-1]
        del snake[-1]
        check_for_food(snake[0])
        check_for_collision(snake[0])


def check_for_collision(head):
    if head in snake[1:] or head[1] == -1 or head[1] == ROWS or head[0] == -1 or head[0] == ROWS:
        game_over()


def game_over():
    gameover_text = WINNING_FONT.render('GAME OVER', 1, (255, 255, 255))
    WIN.blit(gameover_text, (WIN_SIDE_LENGTH/2 - gameover_text.get_width() /
             2, WIN_SIDE_LENGTH/2-gameover_text.get_height()/2))
    gameover_text_score = SMALL_WINNING_FONT.render(
        'SCORE: ' + str(score), 1, (255, 255, 255))
    WIN.blit(gameover_text_score, (WIN_SIDE_LENGTH/2-gameover_text_score.get_width() /
             2, WIN_SIDE_LENGTH/2 + gameover_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    main()


def check_for_food(head):
    global fruit_pos, score
    if fruit_pos == head:
        snake.append(before_tail_cell)
        fruit_pos = []
        score += 1


def draw_window(surface):
    surface.fill((0, 0, 0))
    draw_grid(ROWS, surface, WIN_SIDE_LENGTH)
    draw_fruit()
    draw_snake()
    draw_score()
    pygame.display.update()


def draw_score():
    score_text = SCORE_FONT.render('SCORE: ' + str(score), 1, (255, 255, 255))
    WIN.blit(score_text, (5, 5))


def draw_grid(rows, surface, win_side_length):
    x, y = 0, 0
    for i in range(rows):
        x += CELL_SIZE
        y += CELL_SIZE

        pygame.draw.line(surface, (100, 100, 100),
                         (x, 0), (x, win_side_length))
        pygame.draw.line(surface, (100, 100, 100),
                         (0, y), (win_side_length, y))


def main():
    clock = pygame.time.Clock()
    run = True
    global fruit_pos, snake, direction, before_tail_cell, score
    fruit_pos = []
    snake = [[random.randint(0, ROWS-1), random.randint(0, ROWS-1)]]
    direction = ''
    before_tail_cell = []
    score = 1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != 'DOWN':
                        direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    if direction != 'UP':
                        direction = 'DOWN'
                elif event.key == pygame.K_RIGHT:
                    if direction != 'LEFT':
                        direction = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    if direction != 'RIGHT':
                        direction = 'LEFT'
            if event.type == SNAKE_MOVE:
                move_snake()
        draw_window(WIN)


if __name__ == '__main__':
    main()
