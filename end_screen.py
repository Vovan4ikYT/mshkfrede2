import pygame
import sys
from animation import Animation

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))

images = [pygame.image.load('gifs/static/static1.gif'),
          pygame.image.load('gifs/static/static2.gif'),
          pygame.image.load('gifs/static/static3.gif'),
          pygame.image.load('gifs/static/static4.gif')]

rects = [images[0].get_rect(center=(960, 540)),
         images[1].get_rect(center=(960, 540)),
         images[2].get_rect(center=(960, 540)),
         images[3].get_rect(center=(960, 540))]

gif = Animation(images, 1)

surf = pygame.image.load('screens/game_over_night5_boss.png')
rect = surf.get_rect(center=(960, 540))
font = pygame.font.Font('font2.ttf', 50)
text = font.render('Я ВСЕГДА ВОЗВРАЩАЮСЬ.', True, '#842593')

pygame.mixer.music.load('sounds/static_sound.mp3')
pygame.mixer.music.play()

while True:
    if pygame.time.get_ticks() < 21500:
        gif.change(0.1)
        screen.blit(gif.image, rects[images.index(gif.image)])
        pygame.display.update()
    elif 21500 <= pygame.time.get_ticks() <= 29999:
        screen.blit(surf, rect)
        screen.blit(text, (1250, 1010))
        pygame.display.update()
    elif pygame.time.get_ticks() > 30000:
        import main_menu
        sys.exit()