import pygame
import sys
from random import choice
from animation import Animation
from jumpscares import old_freddy, old_bonnie, old_chica, old_foxy

pygame.mixer.init(channels=4)
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

freddy_gif = Animation(old_freddy, time_interval=0.5)
bonnie_gif = Animation(old_bonnie, time_interval=0.7)
chica_gif = Animation(old_chica, time_interval=0.1)
foxy_gif = Animation(old_foxy, time_interval=9)

count = 0
am = 0
am_count = 15000
speak = 0
speak_count = 500
font = pygame.font.Font('font.otf', 50)

vhs_images1 = [pygame.image.load('vhs/vhs1.jpg'),
               pygame.image.load('vhs/vhs2.jpg'),
               pygame.image.load('vhs/vhs3.jpg'),
               pygame.image.load('vhs/vhs4.jpg'),
               pygame.image.load('vhs/vhs5.jpg')]
vhs_images2 = [pygame.image.load('vhs/vhs6.jpg'),
               pygame.image.load('vhs/vhs7.jpg')]
flashlight_surf = pygame.image.load('flashlight.png')
breaker = pygame.image.load('breaker.jpg')
break_flag = True

vhs_effect1 = Animation(vhs_images1, time_interval=10)
vhs_effect2 = Animation(vhs_images2, time_interval=10)
ambience = pygame.mixer.Sound('sounds/ambience_night4.mp3')
pygame.mixer.Channel(0).play(ambience, loops=-1)

foxy_count, foxy_state = 2000, False
foxy_moves = pygame.image.load('gifs/old_foxy/old_foxy1.png')

freddy_moves = {0: pygame.image.load('gifs/old_freddy/old_freddy1.png'),
                1: pygame.image.load('gifs/old_freddy/old_freddy2.png'),
                2: pygame.image.load('gifs/old_freddy/old_freddy3.png')}
freddy_count, freddy_state = 4000, 0
bc_count = 9000
bc = ''

lines = []
with open('night4.txt', encoding='utf-8') as f:
    for line in f:
        lines.append(line.rstrip('\n'))


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
    if 0 < foxy_count < 800 and count % 2 == 0:
        screen.blit(foxy_moves, (1159, 359))
    if foxy_count == 0 and foxy_state is True:
        foxy_death()


def freddy_death():
    pygame.mixer.Channel(1).stop()
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
    sys.exit()


def freddy_move():
    global freddy_count, freddy_state
    freddy_count -= 1
    if freddy_count % 1000 == 0:
        freddy_state += 1
        if freddy_state == 3:
            freddy_death()
        elif freddy_state == 2:
            if count % 2 != 0:
                state2 = pygame.mixer.Sound('sounds/old_freddy_state2.mp3')
                pygame.mixer.Channel(1).play(state2)
            else:
                state2 = pygame.mixer.Sound('sounds/old_freddy_music_box.mp3')
                pygame.mixer.Channel(1).play(state2)
    try:
        if count % 2 != 0:
            if freddy_state == 0 or freddy_state == 1:
                freddy_x, freddy_y = 516, 311
            else:
                freddy_x, freddy_y = 0, 0
            screen.blit(freddy_moves[freddy_state], (freddy_x, freddy_y))
    except KeyError:
        freddy_death()


def bonnie_death():
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


def chica_death():
    global break_flag, bc_count, bc
    scream = pygame.mixer.Sound('sounds/jumpscares/old_chica_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for j in range(11):
        chica_gif.change(0.5)
        screen.fill((0, 0, 0))
        screen.blit(chica_gif.image, (0, 0))
        pygame.display.update()
    break_flag = False
    bc_count = 9000
    bc = ''
    stun = pygame.mixer.Sound('sounds/stun.mp3')
    pygame.mixer.Channel(0).play(stun, loops=-1)


def bc_move():
    global bc_count, bc
    bc_count -= 1
    if bc_count == 3000:
        steps = pygame.mixer.Sound('sounds/walking.mp3')
        pygame.mixer.Channel(3).play(steps)
        bc = choice(['bonnie', 'chica'])
    elif 0 < bc_count < 3000:
        if count % 2 != 0:
            if bc == 'bonnie':
                screen.blit(pygame.image.load('gifs/old_bonnie/old_bonnie1.png'), (0, 685))
            elif bc == 'chica':
                screen.blit(pygame.image.load('gifs/old_chica/old_chica1.png'), (0, 685))
            pygame.display.update()
    elif bc_count == 0:
        if bc == 'bonnie':
            bonnie_death()
        elif bc == 'chica':
            bc_count = 9000
            bc = ''


def breaking():
    global foxy_count, foxy_state
    if break_flag is True:
        flash = pygame.mixer.Sound('sounds/flash.mp3')
        pygame.mixer.Channel(2).play(flash)
        screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))
        pygame.display.update()
        pygame.time.delay(100)
        if foxy_state is True:
            foxy_state = False
            foxy_count = 2000
        else:
            pygame.mixer.Channel(0).stop()
            pygame.time.delay(10000)
            foxy_death()
    else:
        pass


def flashlight(position):
    global freddy_count, freddy_state, bc, bc_count
    screen.blit(flashlight_surf, flashlight_surf.get_rect(center=position))
    pygame.display.update()
    if (freddy_state == 0 and
            (pygame.mouse.get_pos()[0] in range(675, 1160) and pygame.mouse.get_pos()[1] in range(615, 620))):
        freddy_death()
    if (freddy_state == 1 and
            (pygame.mouse.get_pos()[0] in range(580, 1190) and pygame.mouse.get_pos()[1] in range(675, 680))):
        freddy_death()
    if (freddy_state == 2 and
            (pygame.mouse.get_pos()[0] in range(820, 840) and pygame.mouse.get_pos()[1] in range(560, 570) or
            (pygame.mouse.get_pos()[0] in range(1460, 1480) and pygame.mouse.get_pos()[1] in range(480, 490)))):
        state2 = pygame.mixer.Sound('sounds/old_freddy_state2.mp3')
        pygame.mixer.Channel(1).play(state2)
        freddy_state = 0
        freddy_count = 4000
    if pygame.mouse.get_pos()[0] in range(0, 320) and pygame.mouse.get_pos()[1] in range(940, 950):
        print(bc)
        if bc == 'bonnie':
            bc = ''
            bc_count = 9000
        elif bc == 'chica':
            chica_death()
        else:
            pass


def speaking():
    global speak, speak_count
    if am != 0:
        if lines[speak].isupper() is True:
            screen.blit(font.render(lines[speak], True, 'red'),
                        (0, 1030))
        else:
            screen.blit(font.render(lines[speak], True, 'white'),
                        (0, 1030))
        pygame.display.update()
        speak_count -= 1
        if speak_count == 0:
            speak += 1
            speak_count = 500


while True:
    if count % 2 != 0:
        flashlight(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            print(event.pos)
            if event.pos[0] in range(940, 975) and event.pos[1] in range(633, 635) and count % 2 == 0:
                breaking()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            count += 1
            if count % 2 != 0:
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

    clock.tick(60)
    am_count -= 5
    print(am_count)
    if am_count == 0:
        am += 1
        am_count = 15000
        if am == 6:
            pygame.mixer.Channel(0).stop()
            if pygame.mouse.get_visible() is False:
                pygame.mouse.set_visible(True)
            import sixam
            sys.exit()
    if count % 2 == 0:
        vhs_effect1.change(0.7)
        screen.blit(vhs_effect1.image, (0, 0))
        screen.blit(breaker, (935, 610))
    else:
        vhs_effect2.change(0.7)
        screen.blit(vhs_effect2.image, (0, 0))
    foxy_move()
    freddy_move()
    bc_move()
    am_text = font.render(f'{am}:00 AM', True, 'white')
    screen.blit(am_text, (1680, 0))
    speaking()
    pygame.display.update()