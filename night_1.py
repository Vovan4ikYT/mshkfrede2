# 1 ночь
import os
import pygame
import sqlite3
from random import choice
from jumpscares import freddy, chica
from animation import Animation
from cutscene import Cutscene
import sys

pygame.init()
pygame.mixer.init()

# Создание экрана
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '1' ''').fetchall()  # Текущая ночь
cur.execute('''UPDATE night_info SET current = NULL WHERE night NOT LIKE '1' ''').fetchall()  # Остальные не текущие
con.commit()

# Звуки, изображения
ambient = pygame.mixer.Sound('music/night1amb.mp3')
ambient.play(loops=-1)
shock = pygame.mixer.Sound('sounds/shock.mp3')
no_energy = pygame.mixer.Sound('sounds/nocharge.mp3')
zapis = pygame.mixer.Sound('sounds/nightfm1.mp3')
zapis.play()
background_image = pygame.image.load("ofices/ofice1_night1.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
sounds_folder = "sounds"
fred_warns = [os.path.join(sounds_folder, "fredwarn_1.mp3"),
              os.path.join(sounds_folder, "fredwarn_2.mp3"),
              os.path.join(sounds_folder, "fredwarn_3.mp3")]
chik_warns = [os.path.join(sounds_folder, "chikwarn_1.mp3"),
              os.path.join(sounds_folder, "chikwarn_2.mp3"),
              os.path.join(sounds_folder, "chikwarn_3.mp3")]

# Часы, время в игре
font_time = pygame.font.Font('font.otf', 36)

clock = pygame.time.Clock()
FPS = 60

cooldown = 0  # Перезарядка тока

am = 0  # Текущий час
am_count = 0  # Протекание

counter = 2500  # Скорость аниматроников
door = None  # Сторона
fred_office, chik_office = False, False  # Аниматроник в офисе

# Катсцена
cutscene = Cutscene('cutscenes/cutscene_night1.mp4', 'sounds/cutscenes/cutscene_night1.mp3')


# Скример Фредди
def freddy_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    freddy_gif = Animation(freddy, time_interval=15)
    pygame.mixer.music.stop()
    scream = pygame.mixer.Sound('sounds/jumpscares/freddy_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(225):
        freddy_gif.change(1)
        screen.blit(background_image, (0, 0))
        screen.blit(freddy_gif.image, (0, 0))
        pygame.display.update()
    con.close()
    import lose
    sys.exit()


# Скример Чики
def chica_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    chica_gif = Animation(chica, time_interval=8)
    pygame.mixer.music.stop()
    scream = pygame.mixer.Sound('sounds/jumpscares/chica_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(64):
        chica_gif.change(1)
        screen.blit(background_image, (0, 0))
        screen.blit(chica_gif.image, (0, 0))
        pygame.display.update()
    con.close()
    import lose
    sys.exit()


# Основной цикл
while True:
    # Смена времени
    am_count += 5
    if am_count == 12500:
        am += 1
        am_count = 0

        # Победа
        if am == 6:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            cur.execute('''UPDATE night_info SET unlockation = 'unlocked' WHERE night = '2' ''').fetchall()
            cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '2' ''').fetchall()  # Текущая ночь
            cur.execute(
                '''UPDATE night_info SET current = NULL WHERE night NOT LIKE '2' ''').fetchall()  # Остальные не текущие
            con.commit()
            con.close()
            cutscene.play_cutscene()
            import start_night
            sys.exit()

    # Атака аниматроников
    counter -= 1
    if counter == 1250:
        door = choice(['left', 'right'])
        if door == 'left':
            warn = pygame.mixer.Sound(choice(fred_warns))
            fred_office = True
        elif door == 'right':
            warn = pygame.mixer.Sound(choice(chik_warns))
            chik_office = True
        warn.play()
    if counter == 0:
        if fred_office is True:
            freddy_death()
        elif chik_office is True:
            chica_death()

    for event in pygame.event.get():
        # Выход из ночи
        if event.type == pygame.QUIT:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            con.close()
            import main_menu
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            con.close()
            import main_menu
            sys.exit()
        # Шок аниматроников
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if 224 <= event.pos[0] <= 329 and 311 <= event.pos[1] <= 427:
                if cooldown == 0:  # Если ток не перезаряжается
                    cooldown = 500
                    shock.play()
                    if fred_office is True:
                        fred_office = False
                        counter = 2500
                else:
                    no_energy.play()
            elif 1576 <= event.pos[0] <= 1678 and 449 <= event.pos[1] <= 567:
                if cooldown == 0:
                    cooldown = 500
                    shock.play()
                    if chik_office is True:
                        chik_office = False
                        counter = 2500
                else:
                    no_energy.play()
            elif 1230 <= event.pos[0] <= 1245 and 934 <= event.pos[1] <= 941:
                # Миниигра
                for channel in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(channel).stop()
                con.close()
                import minigame_1

    # Перезарядка тока
    if cooldown != 0:
        cooldown -= 1

    # Отображение
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    time_text = font_time.render(f"{am}:00 AM", True,
                                 (255, 255, 255))
    screen.blit(time_text, (screen_width - time_text.get_width() - 90, 10))
    pygame.display.update()
    clock.tick(FPS)
