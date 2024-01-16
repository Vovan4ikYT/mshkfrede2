import pygame
import sys
import sqlite3
from random import choice
from animation import Animation
from cutscene import Cutscene
from jumpscares import freddy, chica, mangle, candy

pygame.mixer.init(channels=4)
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '5' ''').fetchall()  # Текущая ночь
cur.execute('''UPDATE night_info SET current = NULL WHERE night NOT LIKE '5' ''').fetchall()  # Остальные не текущие
con.commit()

# Мигающий свет в офисе
images = [pygame.image.load('office_night5/office2.png'),
          pygame.image.load('office_night5/office1.png')]

# Звуки
dc = pygame.mixer.Sound('sounds/shock.mp3')

music = pygame.mixer.Sound('music/london_bridge.mp3')
pygame.mixer.Channel(0).set_volume(0.3)
pygame.mixer.Channel(0).play(music)

zapis = pygame.mixer.Sound('sounds/nightfm5.mp3')
pygame.mixer.Channel(4).set_volume(0.2)
pygame.mixer.Channel(4).play(zapis)

# Перезарядка тока
cool = pygame.mixer.Sound('sounds/cooldown.mp3')
cooldown = 0

gif = Animation(images, time_interval=0.5)

# Камеры (не обновляются)
cam_count = 0
cameras = ['cam01', 'cam02', 'cam03', 'cam04', 'cam05', 'cam06', 'cam07',
           'cam01_freddy', 'cam02_freddy', 'cam03_freddy', 'cam04_freddy',
           'cam05_mangle1', 'cam05_mangle2', 'cam05_mangle3',
           'cam06_candy', 'cam07_candy']
cam_surfs = [pygame.image.load('cameras/empty/cam01_empty.png'),
             pygame.image.load('cameras/empty/cam02_empty.png'),
             pygame.image.load('cameras/empty/cam03_empty.png'),
             pygame.image.load('cameras/empty/cam04_empty.png'),
             pygame.image.load('cameras/empty/cam05_empty.png'),
             pygame.image.load('cameras/empty/cam06_empty.png'),
             pygame.image.load('cameras/empty/cam07_empty.png'),
             pygame.image.load('cameras/others/cam01_freddy.png'),
             pygame.image.load('cameras/others/cam02_freddy.png'),
             pygame.image.load('cameras/others/cam03_freddy.png'),
             pygame.image.load('cameras/others/cam04_freddy.png'),
             pygame.image.load('cameras/others/cam05_mangle1.png'),
             pygame.image.load('cameras/others/cam05_mangle2.png'),
             pygame.image.load('cameras/others/cam05_mangle3.png'),
             pygame.image.load('cameras/others/cam06_candy.png'),
             pygame.image.load('cameras/others/cam07_candy.png')]
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

# Фредди
fred_counter = 900
fred_positions = ['idle', 'out', choice(['cam03', 'cam04']), choice(['cam01', 'cam02']), 'office']
fred_current = 'idle'

# Кэнди
candy_counter = 800
candy_positions = ['idle', 'out', 'cam07', 'cam06', choice(['left', 'right']), 'office']
candy_current = 'idle'
candy1 = pygame.image.load('gifs/candy/candy_night5_1.png')
candy2 = pygame.image.load('gifs/candy/candy_night5_2.png')

# Мангл
mangle_counter = 1200
mangle_state = 4
mangle_surf = pygame.image.load('gifs/mangle/mangle1.png')

# Чика
chica_counter = 3300
cupcake = pygame.image.load('gifs/chica/cupcake.png')
chica_office = False

# Катсцена
cutscene_night5 = Cutscene('cutscenes/cutscene_night5.mp4', 'sounds/cutscenes/cutscene_night5.mp3')


def freddy_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    freddy_gif = Animation(freddy, time_interval=15)
    scream = pygame.mixer.Sound('sounds/jumpscares/freddy_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(225):
        freddy_gif.change(1)
        screen.blit(gif.image, (0, 0))
        screen.blit(freddy_gif.image, (0, 0))
        pygame.display.update()
    import lose
    sys.exit()


# Атака Фредди
def freddy_move():
    global fred_current, fred_positions
    try:
        fred_current = fred_positions[fred_positions.index(fred_current) + 1]
        if fred_current == 'cam01':
            laugh = pygame.mixer.Sound('sounds/freddy_laugh1.mp3')
            pygame.mixer.Channel(2).play(laugh)
        elif fred_current == 'cam02':
            laugh = pygame.mixer.Sound('sounds/freddy_laugh2.mp3')
            pygame.mixer.Channel(2).play(laugh)
    except IndexError:
        freddy_death()


def chica_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    chica_gif = Animation(chica, time_interval=8)
    scream = pygame.mixer.Sound('sounds/jumpscares/chica_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(64):
        chica_gif.change(1)
        screen.blit(gif.image, (0, 0))
        screen.blit(chica_gif.image, (0, 0))
        pygame.display.update()
    import lose
    sys.exit()


def mangle_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    mangle_gif = Animation(mangle, time_interval=16)
    scream = pygame.mixer.Sound('sounds/jumpscares/mangle_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(256):
        mangle_gif.change(1)
        screen.blit(gif.image, (0, 0))
        screen.blit(mangle_gif.image, (0, 0))
        pygame.display.update()
    import lose
    sys.exit()


# Атака Мангл
def mangle_move():
    global mangle_state
    mangle_state -= 1
    if mangle_state == 0:
        mangle_death()


def candy_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    candy_gif = Animation(candy, time_interval=26)
    scream = pygame.mixer.Sound('sounds/jumpscares/candy_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(676):
        candy_gif.change(1)
        screen.blit(gif.image, (0, 0))
        screen.blit(candy_gif.image, (0, 0))
        pygame.display.update()
    import lose
    sys.exit()


# Атака Кэнди
def candy_move():
    global candy_current, candy_positions
    try:
        candy_current = candy_positions[candy_positions.index(candy_current) + 1]
    except IndexError:
        candy_death()


# Отображение камер
def cam_show():
    if cam_count % 2 != 0:
        rec = cam_surfs[cameras.index(camera)]
        screen.blit(rec, (0, 0))
        pygame.display.update()


while True:
    # Победа
    if not pygame.mixer.Channel(0).get_busy():
        cutscene_night5.play_cutscene()
        con.close()
        import night5_bossfight
        sys.exit()

    # Атаки аниматроников
    fred_counter -= 1
    if fred_counter == 0:
        freddy_move()
        fred_counter = 900
    mangle_counter -= 1
    if mangle_counter == 0:
        mangle_move()
        mangle_counter = 700
    candy_counter -= 1
    if candy_counter == 0:
        candy_move()
        candy_counter = 800
    chica_counter -= 1
    if chica_counter == 500:
        chica_office = True
    if chica_counter == 0:
        chica_office = False
        chica_counter = 3000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            con.close()
            import main_menu
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

            # Ток
            if event.pos[0] in range(385, 443) and event.pos[1] in range(620, 650):
                if cooldown == 0:
                    pygame.mixer.Channel(1).play(dc)
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    if fred_current == 'cam01':
                        fred_current = 'idle'
                    if candy_current == 'left':
                        candy_current = 'idle'
                    cooldown = 250
                else:
                    pygame.mixer.Channel(1).play(cool)

            # Ток
            elif event.pos[0] in range(1380, 1429) and event.pos[1] in range(620, 650):
                if cooldown == 0:
                    pygame.mixer.Channel(1).play(dc)
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    if fred_current == 'cam02':
                        fred_current = 'idle'
                    if candy_current == 'right':
                        candy_current = 'idle'
                    cooldown = 250
                else:
                    pygame.mixer.Channel(1).play(cool)

            elif event.pos[0] in range(800, 812) and event.pos[1] in range(706, 709):
                # Миниигра
                for channel in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(channel).stop()
                con.close()
                import minigame_5
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # Ток
            if keys[pygame.K_z]:
                if cooldown == 0:
                    pygame.mixer.Channel(1).play(dc)
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    if mangle_state == 1:
                        mangle_state = 3
                    if chica_office is True:
                        chica_death()
                    cooldown = 250
                else:
                    pygame.mixer.Channel(1).play(cool)

            # Выход из ночи
            elif keys[pygame.K_ESCAPE]:
                con.close()
                import main_menu
                sys.exit()

            # Открытие камер
            elif keys[pygame.K_SPACE]:
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

            # Камеры
            elif keys[pygame.K_1]:
                if cam_count % 2 != 0:
                    if fred_current == 'cam01':
                        camera = 'cam01_freddy'
                    else:
                        camera = 'cam01'
            elif keys[pygame.K_2]:
                if cam_count % 2 != 0:
                    if fred_current == 'cam02':
                        camera = 'cam02_freddy'
                    else:
                        camera = 'cam02'
            elif keys[pygame.K_3]:
                if cam_count % 2 != 0:
                    if fred_current == 'cam03':
                        camera = 'cam03_freddy'
                    else:
                        camera = 'cam03'
            elif keys[pygame.K_4]:
                if cam_count % 2 != 0:
                    if fred_current == 'cam04':
                        camera = 'cam04_freddy'
                    else:
                        camera = 'cam04'
            elif keys[pygame.K_5]:
                if cam_count % 2 != 0:
                    if mangle_state == 4:
                        camera = 'cam05_mangle1'
                    elif mangle_state == 3:
                        camera = 'cam05_mangle2'
                    elif mangle_state == 2:
                        camera = 'cam05_mangle3'
                    else:
                        camera = 'cam05'
            elif keys[pygame.K_6]:
                if cam_count % 2 != 0:
                    if candy_current == 'cam06':
                        camera = 'cam06_candy'
                    else:
                        camera = 'cam06'
            elif keys[pygame.K_7]:
                if cam_count % 2 != 0:
                    if candy_current == 'cam07':
                        camera = 'cam07_candy'
                    else:
                        camera = 'cam07'

    # Перезарядка
    if cooldown != 0:
        cooldown -= 1
    gif.change(0.0005)
    cam_show()
    if cam_count % 2 == 0:
        screen.blit(gif.image, (0, 0))
        if mangle_state == 1:
            screen.blit(mangle_surf, (700, 0))
        if candy_current == 'left':
            screen.blit(candy1, (140, 653))
        elif candy_current == 'right':
            screen.blit(candy2, (1570, 653))
        if chica_office is True:
            screen.blit(cupcake, (810, 964))
    pygame.display.update()
