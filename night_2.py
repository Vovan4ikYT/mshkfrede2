import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()
pygame.mixer.init()
# Размеры экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Цвета
WHITE = (255, 255, 255, 0)  # Прозрачный белый
BLACK = (0, 0, 0, 200)  # Черный с прозрачностью

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Переход между комнатами")

# Загрузка изображений для комнат
image1 = pygame.image.load("screens/room_l.jpg")
image1 = pygame.transform.scale(image1, (SCREEN_WIDTH, SCREEN_HEIGHT))

image2 = pygame.image.load("screens/room_r.jpg")
image2 = pygame.transform.scale(image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
# Начальная комната
current_room = "left-room"
show_message = True
work_progress = 0
# Основной цикл программы
mangle_attack_interval = 5  # 2 минуты и 5 секунд в секундах
mangle_attack_timer = time.time() + mangle_attack_interval
mangle_attack_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, было ли нажатие кнопки мыши
            x, y = pygame.mouse.get_pos()

            print(event.pos)
            # Проверяем, по какой комнате было нажатие
            if current_room == "left-room" and 1295 < x < 1903 and 958 < y < 984:
                shag.play()  # Воспроизводим звуковой эффект
                current_room = "right-room"
            elif current_room == "right-room" and 36 < x < 617 and 951 < y < 987:
                shag.play()  # Воспроизводим звуковой эффект
                current_room = "left-room"

            elif current_room == "right-room" and 807 < x < 943 and 560 < y < 803:
                work.play()  # Воспроизводим звуковой эффект
                work_progress += 1  # Увеличиваем прогресс работы
                show_message = False

    # Отрисовка текущей комнаты
    screen.fill(WHITE)

    if current_room == "left-room":
        screen.blit(image1, (0, 0))
        text = font.render("Перейти в правую комнату", True, (255, 255, 255))
        screen.blit(text, (1300, 955))
    elif current_room == "right-room":
        screen.blit(image2, (0, 0))
        text = font.render("Перейти в левую комнату", True, (255, 255, 255))
        screen.blit(text, (42, 955))
        if show_message:
            message = font.render("Кликай на этот ящик", True, (255, 255, 255))
            screen.blit(message, ((SCREEN_WIDTH - message.get_width()) // 2, SCREEN_HEIGHT // 2))

    work_percent = float(work_progress / 300) * 100
    work_str = str(work_percent)
    work_percents = work_str[:4]

    text_percent = font.render(f"Работа: {work_percents}%", True, (255, 255, 255))
    screen.blit(text_percent, (SCREEN_WIDTH - text_percent.get_width() - 20, 20))

    if work_progress >= 300:
        pygame.quit()
        sys.exit()

    current_time = time.time()
    if current_time > mangle_attack_timer and not mangle_attack_active:
        mangle_attack_active = True
        sound2.play()
        mangle_attack_timer = current_time + random.uniform(2, 5)

        if current_room == "right-room":
            # Если игрок в правой комнате, даем ему 3 секунды на переход в левую комнату
            time_limit = current_time + 3

            waiting_for_transition = True
            if current_time > mangle_attack_timer and not mangle_attack_active:
                mangle_attack_active = True
                sound2.play()
                mangle_attack_timer = current_time + random.uniform(2, 5)
                if current_room == "left-room":
                    mangle_attack_active = False

                if current_room == "right-room":
                    # Если игрок в правой комнате, даем ему 3 секунды на переход в левую комнату
                    time_limit = current_time + 3

                    while time.time() < time_limit:
                        pass

                    # Если игрок не перешел в левую комнату за 3 секунды, завершаем игру
                    if current_room == "right-room":
                        pygame.quit()
                        sys.exit()

                    elif current_room == "left-room":
                        mangle_attack_active = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)
