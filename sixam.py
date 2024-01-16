# УРАААААААААААААААААААААААААААА МЕНЯ НЕ СЪЕЛ МИШКА ФРЕДЕ

import pygame
import sys

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))

# эПичНыЙ пЕрЕхОд с 5 нА 6 уТрА
am = 5
am_count = 10000
font = pygame.font.Font('font_main.ttf', 100)

pygame.mixer.music.load('sounds/6am.mp3')
pygame.mixer.music.play()

while True:
    screen.blit(font.render(f'{am} AM', True, 'white'), (760, 540))
    pygame.display.update()
    am_count -= 1
    if am_count == 5000:
        screen.fill((0, 0, 0))
        am += 1
    if am_count == 0:
        import main_menu
        sys.exit()
