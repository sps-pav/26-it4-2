import pygame
import db

# Barvy
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (50, 100, 255)
GRAY = (100, 100, 100)

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

        draw_text(screen, "TETRIS", 50, 60)
        draw_text(screen, "1 - START", 30, 160)

        # Top 5 z databáze
        draw_text(screen, "TOP 5", 25, 250)
        top = db.get_top_scores(5)
        for i, (name, score) in enumerate(top):
            draw_text(screen, str(i + 1) + ". " + name + " - " + str(score), 20, 290 + i * 30)

        draw_text(screen, "ESC - EXIT", 20, 520)

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

# Zadání jména po konci hry
# Vrací napsané jméno (nebo None, když hráč zavře okno)
def name_input(screen, score):
    name = ""

    while True:
        screen.fill(BLACK)

        draw_text(screen, "GAME OVER", 45, 120)
        draw_text(screen, "Score: " + str(score), 30, 200)
        draw_text(screen, "Zadej jméno:", 25, 280)
        draw_text(screen, name + "_", 35, 330)
        draw_text(screen, "ENTER - uložit", 20, 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # prázdné jméno nahradíme výchozím
                    return name.strip() if name.strip() else "Anonym"

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                # max 10 znaků, jen běžné vypsatelné znaky
                elif len(name) < 10 and event.unicode.isprintable() and event.unicode != "":
                    name += event.unicode

        pygame.display.update()

# Zobrazení nově získaných úspěchů po uložení hry
def show_achievements(screen, names):
    while True:
        screen.fill(BLACK)

        draw_text(screen, "NOVÝ ÚSPĚCH!", 35, 120)
        for i, ach in enumerate(names):
            draw_text(screen, ach, 25, 210 + i * 40)
        draw_text(screen, "Stiskni libovolnou klávesu", 18, 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return

        pygame.display.update()
