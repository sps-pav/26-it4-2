
import pygame

# Barvy
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (50, 100, 255)
GRAY = (100, 100, 100)

# Načtení highscore
def get_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# Uložení highscore
def save_highscore(score):
    if score > get_highscore():
        with open("highscore.txt", "w") as file:
            file.write(str(score))

# Vykreslení textu
def draw_text(screen, text, size, y):
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, WHITE)
    screen.blit(surface, (150 - surface.get_width() // 2, y))

# Hlavní menu
def main_menu(screen):
    running = True

    while running:
        screen.fill(BLACK)

        draw_text(screen, "TETRIS", 50, 120)
        draw_text(screen, "1 - START", 30, 250)
        draw_text(screen, "HIGH SCORE: " + str(get_highscore()), 22, 330)
        draw_text(screen, "ESC - EXIT", 20, 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_RETURN:
                    return True

                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()

# Pauza
def pause_menu(screen):
    paused = True

    while paused:
        screen.fill(BLACK)

        draw_text(screen, "PAUSED", 45, 150)
        draw_text(screen, "P - CONTINUE", 25, 270)
        draw_text(screen, "ESC - EXIT", 25, 340)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True

                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()
