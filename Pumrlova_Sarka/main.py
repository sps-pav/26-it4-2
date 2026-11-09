
import pygame
import sys

pygame.init()

# Nastavení hry
WIDTH, HEIGHT = 800, 600
TILE = 40
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moje pixelová adventura")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# Barvy
GREEN = (70, 140, 70)
DARK_GREEN = (35, 90, 45)
BROWN = (120, 75, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (240, 210, 70)

# Hráč
player = pygame.Rect(100, 100, 30, 30)
speed = 4

# Stromy – překážky
trees = [
    pygame.Rect(200, 150, 40, 40),
    pygame.Rect(300, 250, 40, 40),
    pygame.Rect(450, 180, 40, 40),
    pygame.Rect(550, 350, 40, 40),
]

# Předměty
items = [
    pygame.Rect(350, 150, 20, 20),
    pygame.Rect(500, 450, 20, 20),
]

inventory = 0

# Herní stavy
MENU = "menu"
GAME = "game"
PAUSE = "pause"

state = MENU


def draw_text(text, x, y, size=32):
    text_surface = pygame.font.Font(None, size).render(
        text, True, WHITE
    )
    screen.blit(text_surface, (x, y))


def draw_world():
    screen.fill(GREEN)

    # Tráva
    for x in range(0, WIDTH, TILE):
        for y in range(0, HEIGHT, TILE):
            pygame.draw.rect(
                screen, GREEN,
                (x, y, TILE, TILE)
            )

    # Stromy
    for tree in trees:
        pygame.draw.rect(screen, DARK_GREEN, tree)

    # Předměty
    for item in items:
        pygame.draw.rect(screen, YELLOW, item)

    # Hráč
    pygame.draw.rect(screen, (80, 100, 220), player)

    draw_text(f"Inventář: {inventory}", 10, 10)
    draw_text("ESC - Pauza", 10, 40, 24)


def move_player(dx, dy):
    # Pohyb vodorovně
    player.x += dx

    for tree in trees:
        if player.colliderect(tree):
            if dx > 0:
                player.right = tree.left
            elif dx < 0:
                player.left = tree.right

    # Pohyb svisle
    player.y += dy

    for tree in trees:
        if player.colliderect(tree):
            if dy > 0:
                player.bottom = tree.top
            elif dy < 0:
                player.top = tree.bottom

    # Hranice obrazovky
    player.clamp_ip(screen.get_rect())


# Hlavní herní smyčka
running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == MENU:
                if event.key == pygame.K_RETURN:
                    state = GAME

            elif state == GAME:
                if event.key == pygame.K_ESCAPE:
                    state = PAUSE

            elif state == PAUSE:
                if event.key == pygame.K_ESCAPE:
                    state = GAME
                if event.key == pygame.K_m:
                    state = MENU

    keys = pygame.key.get_pressed()

    if state == GAME:

        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += speed

        move_player(dx, dy)

        # Sbírání předmětů
        for item in items[:]:
            if player.colliderect(item):
                items.remove(item)
                inventory += 1

        draw_world()

    elif state == MENU:

        screen.fill(BLACK)

        draw_text("MOJE ADVENTURA", 260, 180, 48)
        draw_text("ENTER - Nova hra", 290, 280)
        draw_text("ESC - Ukoncit hru", 290, 330)

        if keys[pygame.K_ESCAPE]:
            running = False

    elif state == PAUSE:

        screen.fill(BLACK)

        draw_text("PAUZA", 350, 200, 48)
        draw_text("ESC - Pokracovat", 280, 280)
        draw_text("M - Hlavni menu", 280, 330)

    pygame.display.flip()


pygame.quit()
sys.exit()
