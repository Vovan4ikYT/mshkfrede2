import pygame
import sys
from random import choice
from animation import Animation

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
font1 = pygame.font.Font('font.otf', 30)
font2 = pygame.font.Font('font2.ttf', 30)
y = 0
count = choice(range(0, 1000))

babygeist = pygame.image.load('gifs/baby/babygeist.png')
flumpty_images = [pygame.image.load('gifs/flumpty/flumpty1.png'),
                  pygame.image.load('gifs/flumpty/flumpty2.png'),
                  pygame.image.load('gifs/flumpty/flumpty3.png'),
                  pygame.image.load('gifs/flumpty/flumpty4.png')]
flumpty_gif = Animation(flumpty_images, time_interval=16)
rare = ''

with open('warning.txt', encoding='utf-8') as f:
    lines = f.readlines()

if count > 1:
    for i in lines[:3]:
        screen.blit(font1.render(i.rstrip('\n'), True, 'white'), (500, y))
        y += 50
    y = 730
    for i in lines[3:]:
        screen.blit(font2.render(i.rstrip('\n'), True, '#ffffa0'), (500, y))
        y += 50
else:
    rare = choice(['flumpty', 'babygeist'])
    if rare == 'flumpty':
        screen.blit(flumpty_gif.image, (0, 0))
    else:
        screen.blit(babygeist, (0, 0))
    pygame.mixer.music.load('sounds/rare.mp3')
    pygame.mixer.music.play(loops=-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            import main_menu
            sys.exit()

    if rare == 'flumpty':
        flumpty_gif.change(1)
        screen.blit(flumpty_gif.image, (0, 0))
    clock.tick(60)
    pygame.display.update()