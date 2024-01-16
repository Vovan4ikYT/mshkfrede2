# ААААААААААААААААААААААААААААААААААААА МЕНЯ ОПЯТЬ СЪЕЛ МИШКА ФРЕДЕ

import pygame
import sys
from animation import Animation

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))

# Помехи
images = [pygame.image.load('gifs/static/static1.gif'),
          pygame.image.load('gifs/static/static2.gif'),
          pygame.image.load('gifs/static/static3.gif'),
          pygame.image.load('gifs/static/static4.gif')]

gif = Animation(images, 5)
count = 0  # Длительность экрана смерти

surf = pygame.image.load('screens/game_over.png')  # Экран смерти
font = pygame.font.Font('font2.ttf', 50)
text = font.render('ИГРА ОКОНЧЕНА.', True, '#842593')

pygame.mixer.music.load('sounds/static_sound.mp3')
pygame.mixer.music.play()

while True:
    gif.change(0.5)
    screen.blit(gif.image, (0, 0))
    count += 5
    if count >= 15000:
        screen.blit(surf, (0, 0))
        screen.blit(text, (1250, 1010))
    pygame.display.update()
    if count == 17000:
        import main_menu
        sys.exit()
