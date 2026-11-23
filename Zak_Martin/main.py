
import pygame
import random
import menu

# Inicializace hry
pygame.init()

# Nastavení obrazovky
WIDTH = 300
HEIGHT = 600
BLOCK = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Barvy jednotlivých kostek
COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (160, 32, 240),
    (255, 0, 0)
]

# Tvary kostek
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

# Herní plocha
grid = [[0 for x in range(10)] for y in range(20)]

# Nová kostka
def new_piece():
    index = random.randint(0, 6)
    return [SHAPES[index], COLORS[index], 3, 0]

piece = new_piece()
score = 0
running = True

# Kontrola kolize
def collision(piece, dx, dy):
    shape, color, x, y = piece

    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                nx = x + col + dx
                ny = y + row + dy

                if nx < 0 or nx >= 10 or ny >= 20:
                    return True

                if ny >= 0 and grid[ny][nx]:
                    return True

    return False

# Uložení kostky
def place_piece(piece):
    shape, color, x, y = piece

    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] and y + row >= 0:
                grid[y + row][x + col] = color

# Odstranění plných řádků
def clear_lines():
    global grid, score

    new_grid = [row for row in grid if not all(row)]

    removed = 20 - len(new_grid)
    score += removed * 100

    for i in range(removed):
        new_grid.insert(0, [0 for x in range(10)])

    grid = new_grid

# Hlavní menu
if not menu.main_menu(screen):
    pygame.quit()
    quit()

# Hlavní smyčka hry
fall_time = 0

while running:
    screen.fill((20, 20, 20))
    fall_time += clock.get_time()

    # Ovládání
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Pohyb doleva
            if event.key == pygame.K_LEFT:
                if not collision(piece, -1, 0):
                    piece[2] -= 1

            # Pohyb doprava
            if event.key == pygame.K_RIGHT:
                if not collision(piece, 1, 0):
                    piece[2] += 1

            # Rychlejší padání
            if event.key == pygame.K_DOWN:
                if not collision(piece, 0, 1):
                    piece[3] += 1

            # Otočení kostky
            if event.key == pygame.K_UP:
                rotated = piece[0]
                piece[0] = [list(row) for row in zip(*rotated[::-1])]

                if collision(piece, 0, 0):
                    piece[0] = rotated

            # Pauza
            if event.key == pygame.K_p:
                if not menu.pause_menu(screen):
                    running = False

    # Padání kostky
    if fall_time > 500:
        if not collision(piece, 0, 1):
            piece[3] += 1
        else:
            place_piece(piece)
            clear_lines()
            piece = new_piece()

            # Kontrola konce hry
            if collision(piece, 0, 0):
                running = False

        fall_time = 0

    # Vykreslení herní plochy
    for y in range(20):
        for x in range(10):
            color = grid[y][x] if grid[y][x] else (40, 40, 40)

            pygame.draw.rect(
                screen, color,
                (x * BLOCK, y * BLOCK, BLOCK - 1, BLOCK - 1)
            )

    # Vykreslení aktuální kostky
    shape, color, px, py = piece

    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x]:
                pygame.draw.rect(
                    screen, color,
                    ((px + x) * BLOCK, (py + y) * BLOCK,
                     BLOCK - 1, BLOCK - 1)
                )

    # Zobrazení skóre
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (5, 5))

    pygame.display.update()
    clock.tick(60)

# Uložení nejlepšího skóre
menu.save_highscore(score)

pygame.quit()
