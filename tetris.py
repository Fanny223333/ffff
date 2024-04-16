import pygame
import random

# Initialize the game
pygame.init()

# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Define block properties
BLOCK_SIZE = 30
ROWS = WINDOW_HEIGHT // BLOCK_SIZE
COLS = WINDOW_WIDTH // BLOCK_SIZE

# Define tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 1], [0, 0, 1]],  # L shape
    [[1, 1, 1], [1, 0, 0]],  # J shape
]

# Define initial variables
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
current_piece = None
current_shape = None
current_row = 0
current_col = 0
score = 0
grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                GAME_WINDOW,
                grid[row][col],
                pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )


def draw_piece():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                pygame.draw.rect(
                    GAME_WINDOW,
                    current_piece,
                    pygame.Rect(
                        (current_col + col) * BLOCK_SIZE,
                        (current_row + row) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )


def is_collision():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if (
                current_shape[row][col]
                and (
                    current_row + row >= ROWS
                    or current_col + col < 0
                    or current_col + col >= COLS
                    or grid[current_row + row][current_col + col] != BLACK
                )
            ):
                return True
    return False


def rotate_shape(direction):
    if direction == "clockwise":
        return list(zip(*reversed(current_shape)))
    elif direction == "counterclockwise":
        return list(reversed(list(zip(*current_shape))))


def place_piece():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                grid[current_row + row][current_col + col] = current_piece


def check_rows():
    global score
    full_rows = [
        row for row in range(ROWS) if all(grid[row][col] != BLACK for col in range(COLS))
    ]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * COLS)
        score += 100


def draw_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    GAME_WINDOW.blit(score_text, (10, 10))


def game_over():
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    GAME_WINDOW.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))

    pygame.display.flip()
    pygame.time.delay(2000)


def run_game():
    global fall_time, current_piece, current_shape, current_row, current_col, score

    # Initial piece
    current_piece = random.choice([RED, GREEN, BLUE, CYAN, ORANGE, YELLOW, MAGENTA])
    current_shape = random.choice(SHAPES)
    current_row = 0
    current_col = COLS // 2 - len(current_shape[0]) // 2

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_col -= 1
                    if is_collision():
                        current_col += 1
                elif event.key == pygame.K_RIGHT:
                    current_col += 1
                    if is_collision():
                        current_col -= 1
                elif event.key == pygame.K_DOWN:
                    current_row += 1
                    if is_collision():
                        current_row -= 1
                elif event.key == pygame.K_UP:
                    current_shape = rotate_shape("clockwise")
                    if is_collision():
                        current_shape = rotate_shape("counterclockwise")

        # Update
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 500 >= fall_speed:
            current_row += 1
            fall_time = 0
            if is_collision():
                current_row -= 1
                place_piece()
                check_rows()
                if current_row <= 0:
                    running = False
                else:
                    current_piece = random.choice(
                        [RED, GREEN, BLUE, CYAN, ORANGE, YELLOW, MAGENTA]
                    )
                    current_shape = random.choice(SHAPES)
                    current_row = 0
                    current_col = COLS // 2 - len(current_shape[0]) // 2

        # Render
        GAME_WINDOW.fill(BLACK)
        draw_grid()
        draw_piece()
        draw_score()
        pygame.display.flip()

    game_over()

    # Quit the game
    pygame.quit()


# Run the game
run_game()
