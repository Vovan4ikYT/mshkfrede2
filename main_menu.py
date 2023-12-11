import pygame
import sys
from random import choice
from animation import Animation

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

night = 5
if night == 5:
    anim = 'springtrap'
    color = 'lime'
    pygame.mixer.music.load('music/the_hunt.mp3')
else:
    anim = choice(['freddy', 'baby', 'candy'])
    color = 'deepskyblue'
    pygame.mixer.music.load('music/mechanical_instinct.mp3')

images = [pygame.image.load(f'gifs/{anim}/{anim}1.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}2.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}3.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}4.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}5.gif')]

rects = [images[0].get_rect(center=(960, 540)),
         images[1].get_rect(center=(960, 540)),
         images[2].get_rect(center=(960, 540)),
         images[3].get_rect(center=(960, 540)),
         images[4].get_rect(center=(960, 540))]

gif = Animation(images, 1)

font1, font2 = pygame.font.Font('font_main.ttf', 50), pygame.font.Font('font.otf', 50)
text1, text2, text3, text4 = (font1.render('FREDDYS RETURN', True, color),
                              font2.render('ЗНАКОМОЕ МЕСТО', True, color),
                              font2.render('Выйти', True, color),
                              font2.render('< ГРОМКОСТЬ >', True, color))

pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            print(i.pos)
            if i.pos[0] in range(0, 190) and i.pos[1] in range(1030, 1080):
                sys.exit()
            elif i.pos[0] in range(1485, 1515) and i.pos[1] in range(795, 845):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
            elif i.pos[0] in range(1885, 1915) and i.pos[1] in range(795, 845):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

    clock.tick(60)
    move = choice(range(0, 100))
    if move <= 5:
        gif.change(10)
        screen.blit(gif.image, rects[images.index(gif.image)])
        screen.blit(text1, (1280, 0))
        screen.blit(text2, (1380, 70))
        screen.blit(text3, (0, 1030))
        screen.blit(text4, (1490, 800))
        pygame.display.update()
