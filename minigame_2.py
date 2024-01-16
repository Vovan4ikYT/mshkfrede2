import pygame
import sys
import time
import sqlite3

pygame.init()

# Определение размеров экрана
screen_width = 1920
screen_height = 1080

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Мини-игра")

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

# Загрузка фона и изображений хождения влево и вправо
background = pygame.image.load("screens/minigame_phone.png")
background = pygame.transform.scale(background, (screen_width, screen_height))
walk_left_sprites = [pygame.image.load(f"sprites/bonnie_left_{i}.png") for i in range(1, 3)]
walk_right_sprites = [pygame.image.load(f"sprites/bonnie_right_{i}.png") for i in range(1, 3)]
static_character = pygame.image.load("sprites/bonnie_static.png")
sad_children_sprite = pygame.image.load("sprites/sad_children.png")
happy_children_sprite = pygame.image.load("sprites/happy_children.png")
guitar_sprite = pygame.image.load("sprites/guitar.png")
character_scale = 4  # Коэффициент масштабирования
character_scale2 = 2
walk_left_sprites = [
    pygame.transform.scale(sprite, (sprite.get_width() * character_scale, sprite.get_height() * character_scale)) for
    sprite in walk_left_sprites]
walk_right_sprites = [
    pygame.transform.scale(sprite, (sprite.get_width() * character_scale, sprite.get_height() * character_scale)) for
    sprite in walk_right_sprites]
static_character = pygame.transform.scale(static_character, (static_character.get_width() *
                                                             character_scale,
                                                             static_character.get_height() * character_scale))
sad_children_sprite = pygame.transform.scale(sad_children_sprite, (sad_children_sprite.get_width() *
                                                                   character_scale2,
                                                                   sad_children_sprite.get_height() * character_scale2))
happy_children_sprite = pygame.transform.scale(happy_children_sprite, (happy_children_sprite.get_width() *
                                                                       character_scale2,
                                                                       happy_children_sprite.get_height() *
                                                                       character_scale2))

# Измените коэффициенты по вашему усмотрению
new_size_guitar = (int(guitar_sprite.get_width() * 0.4), int(guitar_sprite.get_height() * 0.4))
guitar_sprite = pygame.transform.scale(guitar_sprite, new_size_guitar)
# Начальная позиция персонажа
character_x = 1415
character_y = 730

# Флаг для активации
flag_activated = False
change_children_sprite = False
# Переменные для анимации
walk_count = 0
character = None

clock = pygame.time.Clock()
pygame.mixer.music.load("music/minigame_ambient_1.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
# Переменная для отслеживания времени начала события
event_start_time = None
# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # При клике мыши выводим координаты в консоль
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"X:{mouse_x} Y:{mouse_y}")

    keys = pygame.key.get_pressed()

    # Проверка условия для активации флага
    if not flag_activated and character_x == 315 and character_y == 730:
        flag_activated = True
        change_children_sprite = True
        event_start_time = time.time()  # Записываем время начала события

    # Если флаг активирован, выполните нужные действия
    if flag_activated:
        character = static_character  # Персонаж становится неподвижным

        # Замена спрайта sad_children_sprite на happy_children_sprite
        screen.blit(happy_children_sprite, (90, 981))

        # Отображение guitar_sprite по указанным координатам
        screen.blit(guitar_sprite, (868, 527))

        # Проверка времени с начала события
        elapsed_time = time.time() - event_start_time
        if elapsed_time >= 5:
            cur.execute('''UPDATE minigames SET minigame2 = 'unlocked' ''').fetchall()
            con.commit()
            con.close()
            import night_2
            sys.exit()

    else:
        # Перемещение персонажа с анимацией
        if keys[pygame.K_a] and character_x > 0:
            character_x -= 5
            character = walk_left_sprites[walk_count // 5]
        elif keys[pygame.K_d] and character_x < screen_width - walk_right_sprites[0].get_width():
            character_x += 5
            character = walk_right_sprites[walk_count // 5]
        else:
            character = static_character  # Используем первый кадр как статический кадр

    # Отрисовка фона и персонажа
    screen.blit(background, (0, 0))
    if not change_children_sprite:
        screen.blit(sad_children_sprite, (10, 885))
    if change_children_sprite:
        screen.blit(happy_children_sprite, (10, 885))
    screen.blit(character, (character_x, character_y))
    if change_children_sprite:
        screen.blit(guitar_sprite, (150, 920))
    # Увеличение счетчика для анимации
    walk_count = (walk_count + 1) % (len(walk_left_sprites) * 5)
    pygame.display.flip()
    clock.tick(30)
