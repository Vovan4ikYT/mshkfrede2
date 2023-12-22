import pygame
import sys
from random import choice
from animation import Animation
from jumpscares import baby, springtrap1, springtrap2

pygame.mixer.init(channels=2)
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

images = [pygame.image.load('office_night5/office2_boss.png'),
          pygame.image.load('office_night5/office1_boss.png')]

rects = [images[0].get_rect(center=(960, 540)),
         images[1].get_rect(center=(960, 540))]

alert = pygame.image.load('alert.png')

shocks = [pygame.image.load('shock1.png'), pygame.image.load('shock2.png')]
shock_rects = [shocks[0].get_rect(center=(400, 800)), shocks[1].get_rect(center=(1463, 800))]

spring_counter = 90
baby_counter, baby_state = 180, False
power = 100

gif = Animation(images, time_interval=0.5)

music = pygame.mixer.Sound('music/our_little_horror_story.mp3')
pygame.mixer.Channel(0).play(music)

spring_positions = ['idle', 'out', 'cam07', 'cam04', choice(['cam02', 'cam03']), 'office']
spring_current = 'idle'


def spring_death():
    if anim == '1':
        spring_images = springtrap1
    else:
        spring_images = springtrap2
    spring_gif = Animation(spring_images, time_interval=32)
    jumpscare = pygame.mixer.Sound('sounds/jumpscares/spring_jumpscare.mp3')
    pygame.mixer.Channel(0).play(jumpscare)
    alarm = pygame.mixer.Sound('sounds/alarm.mp3')
    pygame.mixer.Channel(1).play(alarm, loops=11)
    for j in range(1024):
        spring_gif.change(1)
        screen.blit(spring_gif.image, (0, 0))
        pygame.display.update()
        gif.change(0.01)
        screen.blit(gif.image, rects[images.index(gif.image)])
    import lose


def baby_death():
    baby_gif = Animation(baby, time_interval=11)
    jumpscare = pygame.mixer.Sound('sounds/jumpscares/baby_jumpscare.mp3')
    pygame.mixer.Channel(0).play(jumpscare)
    for j in range(121):
        baby_gif.change(1)
        screen.blit(baby_gif.image, (0, 0))
        pygame.display.update()
        gif.change(0.01)
        screen.blit(gif.image, rects[images.index(gif.image)])
    import lose


def spring_move():
    global anim, spring_current
    try:
        spring_current = spring_positions[spring_positions.index(spring_current) + 1]
    except IndexError:
        if spring_positions[spring_positions.index(spring_current) - 1] == 'cam02':
            anim = '1'
        else:
            anim = '2'
        spring_death()


def baby_glitching():
    baby_surfs = [pygame.image.load('gifs/baby/glitch1.png'), pygame.image.load('gifs/baby/glitch2.png')]
    baby_rects = [baby_surfs[0].get_rect(center=(950, 700)), baby_surfs[1].get_rect(center=(950, 700))]
    if baby_state is False:
        screen.blit(baby_surfs[0], baby_rects[0])
    else:
        screen.blit(baby_surfs[1], baby_rects[1])


def alertion():
    if spring_current == 'cam02':
        alert_rect = alert.get_rect(center=(100, 50))
        screen.blit(alert, alert_rect)
        pygame.display.update()
    elif spring_current == 'cam03':
        alert_rect = alert.get_rect(center=(1820, 50))
        screen.blit(alert, alert_rect)
        pygame.display.update()


def left_shocker():
    global spring_current, power
    power -= 1
    if spring_current == 'cam02':
        spring_current = 'idle'
    dc = pygame.mixer.Sound('sounds/shock.mp3')
    pygame.mixer.Channel(1).play(dc)


def right_shocker():
    global spring_current, power
    power -= 1
    if spring_current == 'cam03':
        spring_current = 'idle'
    dc = pygame.mixer.Sound('sounds/shock.mp3')
    pygame.mixer.Channel(1).play(dc)


while True:
    spring_counter -= 1
    if spring_counter == 0:
        spring_move()
        spring_counter = 90
    baby_counter -= 2
    if baby_counter == 0:
        if baby_state is False:
            baby_state = True
            baby_counter = 180
        else:
            baby_death()

    power -= 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_z:
                power -= 1
                dc = pygame.mixer.Sound('sounds/shock.mp3')
                pygame.mixer.Channel(1).play(dc)
                if baby_state is True:
                    baby_state = False
                    baby_counter = 180
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if event.pos[0] in range(375, 433) and event.pos[1] in range(640, 667):
                left_shocker()
            elif event.pos[0] in range(1415, 1471) and event.pos[1] in range(640, 667):
                right_shocker()

    clock.tick(60)

    gif.change(0.005)
    screen.blit(gif.image, rects[images.index(gif.image)])
    screen.blit(shocks[0], shock_rects[0])
    screen.blit(shocks[1], shock_rects[1])
    baby_glitching()
    alertion()
    pygame.display.update()
