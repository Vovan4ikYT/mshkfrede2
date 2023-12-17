import pygame
import sys
from random import choice
from animation import Animation
from jumpscares import old_freddy, old_bonnie, old_chica, old_foxy

pygame.mixer.init(channels=3)
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

freddy_gif = Animation(old_freddy, time_interval=0.5)
bonnie_gif = Animation(old_bonnie, time_interval=0.7)
chica_gif = Animation(old_chica, time_interval=0.1)
foxy_gif = Animation(old_foxy, time_interval=9)

vhs_images = [pygame.image.load('vhs/vhs1.jpg'),
              pygame.image.load('vhs/vhs2.jpg'),
              pygame.image.load('vhs/vhs3.jpg'),
              pygame.image.load('vhs/vhs4.jpg'),
              pygame.image.load('vhs/vhs5.jpg'),]

vhs_effect = Animation(vhs_images, time_interval=10)
ambience = pygame.mixer.Sound('sounds/ambience_night4.mp3')
pygame.mixer.Channel(0).play(ambience)
breaker = pygame.image.load('breaker.jpg')

foxy_count, foxy_state = 2000, False
foxy_moves = pygame.image.load('gifs/old_foxy/old_foxy1.png')


def foxy_death():
    scream = pygame.mixer.Sound('sounds/jumpscares/old_foxy_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for j in range(100):
        foxy_gif.change(1)
        screen.fill((0, 0, 0))
        screen.blit(foxy_gif.image, (0, 0))
        pygame.display.update()
    sys.exit()


def foxy_move():
    global foxy_count, foxy_state
    foxy_count -= 1
    if foxy_count == 800:
        foxy_state = True
        foxy_poet = pygame.mixer.Sound('sounds/old_foxy_poet.mp3')
        pygame.mixer.Channel(2).set_volume(0.3)
        pygame.mixer.Channel(2).play(foxy_poet)
    if 0 < foxy_count < 800:
        screen.blit(foxy_moves, (1159, 359))
    if foxy_count == 0 and foxy_state is True:
        foxy_death()


def breaking():
    global foxy_count, foxy_state
    flash = pygame.mixer.Sound('sounds/flash.mp3')
    pygame.mixer.Channel(2).play(flash)
    screen.fill((255, 255, 255))
    pygame.display.update()
    pygame.time.delay(100)
    if foxy_state is True:
        foxy_state = False
        foxy_count = 2000
    else:
        foxy_death()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            print(event.pos)
            if event.pos[0] in range(940, 975) and event.pos[1] in range(633, 635):
                breaking()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            scream = pygame.mixer.Sound('sounds/jumpscares/old_freddy_jumpscare.mp3')
            pygame.mixer.Channel(0).play(scream)
            for j in range(3):
                freddy_gif.change(0.9)
                screen.fill((0, 0, 0))
                screen.blit(freddy_gif.image, (0, 0))
                pygame.display.update()
            freddy_gif.time_interval = 12
            for j in range(144):
                freddy_gif.change(1)
                screen.fill((0, 0, 0))
                screen.blit(freddy_gif.image, (0, 0))
                pygame.display.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            scream = pygame.mixer.Sound('sounds/jumpscares/old_bonnie_jumpscare.mp3')
            pygame.mixer.Channel(0).play(scream)
            for j in range(3):
                bonnie_gif.change(1.1)
                screen.fill((0, 0, 0))
                screen.blit(bonnie_gif.image, (0, 0))
                pygame.display.update()
            bonnie_gif.time_interval = 14
            for j in range(196):
                bonnie_gif.change(4)
                screen.fill((0, 0, 0))
                screen.blit(bonnie_gif.image, (0, 0))
                if j == 63:
                    sys.exit()
                pygame.display.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            scream = pygame.mixer.Sound('sounds/jumpscares/old_chica_jumpscare.mp3')
            pygame.mixer.Channel(0).play(scream)
            for j in range(11):
                chica_gif.change(0.5)
                screen.fill((0, 0, 0))
                screen.blit(chica_gif.image, (0, 0))
                pygame.display.update()

    clock.tick(60)
    vhs_effect.change(0.7)
    screen.blit(vhs_effect.image, (0, 0))
    screen.blit(breaker, (935, 610))
    foxy_move()
    pygame.display.update()