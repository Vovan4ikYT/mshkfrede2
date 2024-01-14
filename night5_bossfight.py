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

dc = pygame.mixer.Sound('sounds/shock.mp3')

spring_counter = 90
surprize = False
baby_counter, baby_state = 180, False

gif = Animation(images, time_interval=0.5)

music = pygame.mixer.Sound('music/our_little_horror_story.mp3')
pygame.mixer.Channel(0).play(music)

spring_positions = ['idle', 'out', 'cam07', 'cam04', choice(['cam02', 'cam03']), choice(['left', 'right']), 'office']
spring_current = 'idle'

cool = pygame.mixer.Sound('sounds/cooldown.mp3')
cooldown = 0

font = pygame.font.Font('font.otf', 50)
am_count = 0
am = 2
cam_count = 0
cameras = ['cam01', 'cam02', 'cam03', 'cam04', 'cam05', 'cam06', 'cam07',
           'cam02_springtrap', 'cam03_springtrap', 'cam04_springtrap', 'cam07_springtrap']
cam_surfs = [pygame.image.load('cameras/empty/cam01_empty.png'),
             pygame.image.load('cameras/empty/cam02_empty.png'),
             pygame.image.load('cameras/empty/cam03_empty.png'),
             pygame.image.load('cameras/empty/cam04_empty.png'),
             pygame.image.load('cameras/empty/cam05_empty.png'),
             pygame.image.load('cameras/empty/cam06_empty.png'),
             pygame.image.load('cameras/empty/cam07_empty.png'),
             pygame.image.load('cameras/springtrap/cam02_springtrap.png'),
             pygame.image.load('cameras/springtrap/cam03_springtrap.png'),
             pygame.image.load('cameras/springtrap/cam04_springtrap.png'),
             pygame.image.load('cameras/springtrap/cam07_springtrap.png')]
camera = 'cam01'

monitor_up = [pygame.image.load('cameras/monitor/up/monitor_up1.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up2.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up3.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up4.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up5.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up6.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up7.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up8.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up9.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up10.gif'),
              pygame.image.load('cameras/monitor/up/monitor_up11.gif')]

monitor_down = [pygame.image.load('cameras/monitor/down/monitor_down1.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down2.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down3.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down4.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down5.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down6.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down7.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down8.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down9.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down10.gif'),
                pygame.image.load('cameras/monitor/down/monitor_down11.gif')]


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
        screen.blit(gif.image, (0, 0))
    import lose


def cam_show():
    if cam_count % 2 != 0:
        rec = cam_surfs[cameras.index(camera)]
        screen.blit(rec, (0, 0))
        pygame.display.update()


def baby_death():
    baby_gif = Animation(baby, time_interval=11)
    jumpscare = pygame.mixer.Sound('sounds/jumpscares/baby_jumpscare.mp3')
    pygame.mixer.Channel(0).play(jumpscare)
    for j in range(121):
        baby_gif.change(1)
        screen.blit(baby_gif.image, (0, 0))
        pygame.display.update()
        gif.change(0.01)
        screen.blit(gif.image, (0, 0))
    import lose


def spring_move():
    global anim, spring_current, surprize
    try:
        spring_current = spring_positions[spring_positions.index(spring_current) + 1]
        surprize = choice([True, False])
    except IndexError:
        if spring_positions[spring_positions.index(spring_current) - 1] == 'left':
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
    global surprize
    if surprize is True:
        alert = pygame.image.load('alert_surprize.png')
    else:
        alert = pygame.image.load('alert.png')
    if spring_current == 'left':
        screen.blit(alert, (100, 0))
        pygame.display.update()
    elif spring_current == 'right':
        screen.blit(alert, (1820, 0))
        pygame.display.update()


def left_shocker():
    global spring_current, cooldown, surprize
    if cooldown == 0:
        if (spring_current == 'left' and surprize is False) or (spring_current == 'right' and surprize is True):
            spring_current = 'idle'
        pygame.mixer.Channel(1).play(dc)
        screen.fill((0, 0, 0))
        pygame.display.update()
        cooldown = 50
    else:
        pygame.mixer.Channel(1).play(cool)


def right_shocker():
    global spring_current, cooldown, surprize
    if cooldown == 0:
        if (spring_current == 'right' and surprize is False) or (spring_current == 'left' and surprize is True):
            spring_current = 'idle'
        pygame.mixer.Channel(1).play(dc)
        screen.fill((0, 0, 0))
        pygame.display.update()
        cooldown = 50
    else:
        pygame.mixer.Channel(1).play(cool)


while True:
    am_count += 5
    if am_count == 7400:
        am += 1
        am_count = 0
        if am == 6:
            import sixam
            sys.exit()
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if event.pos[0] in range(385, 443) and event.pos[1] in range(620, 650):
                left_shocker()
            elif event.pos[0] in range(1380, 1429) and event.pos[1] in range(620, 650):
                right_shocker()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                cam_count += 1
                if cam_count % 2 != 0:
                    monitor = Animation(monitor_up, time_interval=11)
                    for i in range(121):
                        monitor.change(1)
                        screen.blit(monitor.image, (0, 0))
                        pygame.display.update()
                else:
                    monitor = Animation(monitor_down, time_interval=11)
                    for i in range(121):
                        screen.blit(gif.image, (0, 0))
                        monitor.change(1)
                        screen.blit(monitor.image, (0, 0))
                        pygame.display.update()
            elif keys[pygame.K_ESCAPE]:
                sys.exit()
            elif keys[pygame.K_z]:
                if cam_count % 2 == 0:
                    if cooldown == 0:
                        pygame.mixer.Channel(1).play(dc)
                        screen.fill((0, 0, 0))
                        pygame.display.update()
                        cooldown = 50
                        if baby_state is True:
                            baby_state = False
                            baby_counter = 180
                    else:
                        pygame.mixer.Channel(1).play(cool)
            elif keys[pygame.K_1]:
                if cam_count % 2 != 0:
                    camera = 'cam01'
            elif keys[pygame.K_2]:
                if cam_count % 2 != 0:
                    if spring_current == 'cam02':
                        camera = 'cam02_springtrap'
                    else:
                        camera = 'cam02'
            elif keys[pygame.K_3]:
                if cam_count % 2 != 0:
                    if spring_current == 'cam03':
                        camera = 'cam03_springtrap'
                    else:
                        camera = 'cam03'
            elif keys[pygame.K_4]:
                if cam_count % 2 != 0:
                    if spring_current == 'cam04':
                        camera = 'cam04_springtrap'
                    else:
                        camera = 'cam04'
            elif keys[pygame.K_5]:
                if cam_count % 2 != 0:
                    camera = 'cam05'
            elif keys[pygame.K_6]:
                if cam_count % 2 != 0:
                    camera = 'cam06'
            elif keys[pygame.K_7]:
                if cam_count % 2 != 0:
                    if spring_current == 'cam07':
                        camera = 'cam07_springtrap'
                    else:
                        camera = 'cam07'

    clock.tick(60)
    gif.change(0.005)
    cam_show()
    if cam_count % 2 == 0:
        screen.blit(gif.image, (0, 0))
        baby_glitching()
        alertion()
        am_text = font.render(f'{am}:00 AM', True, 'purple')
        screen.blit(am_text, (1680, 100))
    if cooldown != 0:
        cooldown -= 1
    else:
        pass
    pygame.display.update()
