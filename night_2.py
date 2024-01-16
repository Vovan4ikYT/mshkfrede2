# 2 ночь
import pygame
import sys
import sqlite3
from random import choice
from jumpscares import mangle
from animation import Animation

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Размеры экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Переход между комнатами")

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '2' ''').fetchall()  # Текущая ночь
cur.execute('''UPDATE night_info SET current = NULL WHERE night NOT LIKE '2' ''').fetchall()  # Остальные не текущие
con.commit()

# Загрузка изображений для комнат
image1 = pygame.image.load("screens/room_l.jpg")
image1 = pygame.transform.scale(image1, (SCREEN_WIDTH, SCREEN_HEIGHT))

image2 = pygame.image.load("screens/room_r.jpg")
image2 = pygame.transform.scale(image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

froggy = pygame.image.load("gifs/froggy.png")

# Загрузка шрифта
font = pygame.font.Font("font.otf", 36)

# Загрузка звукового эффекта
shag = pygame.mixer.Sound("sounds/pereh.mp3")
work = pygame.mixer.Sound("sounds/work.mp3")
zapis = pygame.mixer.Sound('sounds/nightfm2.mp3')
zapis.play()
pygame.mixer.music.load('music/night2amb.mp3')
pygame.mixer.music.play(-1)
sound2 = pygame.mixer.Sound("sounds/work.mp3")

# Текущая комната
current_room = image1
work_progress = 0
show_message = True
perehod_text = font.render('Перейти в правую комнату', True, (255, 255, 255))

# Мангл и её составляющие
mangle_counter = 2000
mangle_surf = pygame.image.load("gifs/mangle/mangle1.png")
mangle_static = pygame.mixer.Sound("sounds/mangle_static.mp3")
mangle_static.set_volume(0.3)


# Скример Мангл
def mangle_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    mangle_gif = Animation(mangle, time_interval=16)
    scream = pygame.mixer.Sound('sounds/jumpscares/mangle_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(256):
        mangle_gif.change(1)
        screen.blit(current_room, (0, 0))
        screen.blit(mangle_gif.image, (0, 0))
        pygame.display.update()
        con.close()
    import lose
    sys.exit()


# Основной цикл программы
while True:
    # Спавн Мангл
    mangle_counter -= 1
    if mangle_counter == 1000:
        mangle_static.play()
    if mangle_counter > 1000:
        mangle_static.stop()
    if mangle_counter == 0:
        if current_room == image1:
            mangle_counter = 2000
        else:
            mangle_death()
    for event in pygame.event.get():
        # Выход из ночи
        if event.type == pygame.QUIT:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            con.close()
            import main_menu
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for channel in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(channel).stop()
            con.close()
            import main_menu
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, было ли нажатие кнопки мыши
            x, y = pygame.mouse.get_pos()

            print(event.pos)
            # Проверяем, по какой комнате было нажатие
            if current_room == image1 and 1295 < x < 1903 and 958 < y < 984:
                shag.play()  # Воспроизводим звуковой эффект
                current_room = image2
                perehod_text = font.render('Перейти в левую комнату', True, (255, 255, 255))
            elif current_room == image2 and 36 < x < 617 and 951 < y < 987:
                shag.play()  # Воспроизводим звуковой эффект
                current_room = image1
                perehod_text = font.render('Перейти в правую комнату', True, (255, 255, 255))

            elif current_room == image2 and 807 < x < 943 and 560 < y < 803:
                work.play()  # Воспроизводим звуковой эффект
                work_progress += 1  # Увеличиваем прогресс работы
                show_message = False

            elif 1428 <= x <= 1434 and 228 <= y <= 234:
                # Миниигра
                for channel in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(channel).stop()
                con.close()
                import minigame_2

    # Отрисовка текущей комнаты
    screen.fill((255, 255, 255, 0))

    if current_room == image1:
        screen.blit(current_room, (0, 0))
        screen.blit(perehod_text, (1300, 955))
        count = choice(range(0, 1000))
        if count <= 1:
            screen.blit(froggy, (0, 500))
    elif current_room == image2:
        screen.blit(current_room, (0, 0))
        screen.blit(perehod_text, (42, 955))
        if show_message:
            message = font.render("Кликай на этот ящик", True, (255, 255, 255))
            screen.blit(message, ((SCREEN_WIDTH - message.get_width()) // 2, SCREEN_HEIGHT // 2))

    work_percent = float(work_progress / 300) * 100
    work_str = str(work_percent)
    work_percents = work_str[:4]

    text_percent = font.render(f"Работа: {work_percents}%", True, (255, 255, 255))
    screen.blit(text_percent, (SCREEN_WIDTH - text_percent.get_width() - 20, 20))

    # Победа
    if work_progress >= 300:
        for channel in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(channel).stop()
        cur.execute('''UPDATE night_info SET unlockation = 'unlocked' WHERE night = '3' ''').fetchall()
        con.commit()
        con.close()
        import sixam
        sys.exit()

    if 0 < mangle_counter < 1000:
        if current_room == image2:
            screen.blit(mangle_surf, (554, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
