import pygame # Knihovna pro tvorbu her (řeší grafiku, události, okno)
import sys    # Systémová knihovna (potřebná pro tvrdé ukončení programu)

pygame.init() # Inicializuje všechny moduly Pygame

okno = pygame.display.set_mode((960, 640))      # Vytvoří herní okno o rozměrech 960x640 pixelů
pygame.display.set_caption("Penalty Simulator") # Nápis v liště okna
font = pygame.font.SysFont("arial", 40)         # Načte systémový font Arial o velikosti 40
hodiny = pygame.time.Clock()                    # Vytvoří objekt hodin pro hlídání rychlosti hry (FPS)

menu = True                                    # Stavová proměnná: True = jsme v menu, False = hrajeme hru

while True:                                    # Hlavní herní smyčka (běží pořád dokola, dokud hru nevypneš)
    for udalost in pygame.event.get():         # Zjistí všechny akce, co uživatel právě udělal (kliky, klávesy)

        if udalost.type == pygame.QUIT:        # Uživatel klikl na křížek okna
            pygame.quit()                      # Ukončí Pygame moduly
            sys.exit()                         # Tvrdě ukončí celý Python skript

        if udalost.type == pygame.KEYDOWN:     # Uživatel zmáčkl libovolnou klávesu

            if udalost.key == pygame.K_RETURN: # Pokud to byl ENTER...
                menu = False                   # ...přepne hru z menu do samotné hry

            if udalost.key == pygame.K_ESCAPE: # Pokud to byl ESCAPE...
                if menu:                       # ...a jsme zrovna v menu...
                    pygame.quit()              # ...bezpečně vypne hru
                    sys.exit()
                else:                          # ...ale pokud jsme ve hře...
                    menu = True                # ...jen nás vrátí zpět do menu

    # --- VYKRESLOVÁNÍ GRAFIKY ---
    if menu:
        okno.fill((0, 0, 0)) # Vybarví celé okno na černo (R=0, G=0, B=0)
        # Metoda render() vyrobí z textu obrázek. Metoda blit() ten obrázek vykreslí na souřadnice (X, Y).
        okno.blit(font.render("PENALTY SIMULATOR", True, (255, 200, 0)), (280, 180))    # Žlutý nadpis
        okno.blit(font.render("ENTER = Start", True, (255, 255, 255)), (350, 280))      # Bílý text
        okno.blit(font.render("ESC = Konec", True, (255, 255, 255)), (350, 340))        # Bílý text
    else:
        okno.fill((0, 120, 0))  # Vybarví celé okno tmavě zelenou (trávník)
        okno.blit(font.render("Tady bude hra (ESC = menu)", True, (255, 255, 255)), (230, 300)) # Nápověda pro hráče

    pygame.display.flip()   # Vezme všechno, co jsme teď nakreslili v paměti, a zobrazí to na monitoru
    hodiny.tick(60)         # Zpomalí smyčku tak, aby běžela maximálně 60x za vteřinu (60 FPS)