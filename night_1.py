# 1 ночь
import os
import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.music.load('music/night1amb.mp3')
pygame.mixer.music.play(-1)
shock = pygame.mixer.Sound('sounds/shock.mp3')
no_energy = pygame.mixer.Sound('sounds/nocharge.mp3')
zapis = pygame.mixer.Sound('sounds/nightfm1.mp3')
zapis.play()
background_image = pygame.image.load("ofices/ofice1_night1.png").convert()
camera_image = pygame.image.load("screens/hol_l.png").convert()
sounds_folder = "sounds"
fred_warns = [os.path.join(sounds_folder, "fredwarn_1.mp3"),
              os.path.join(sounds_folder, "fredwarn_2.mp3"),
              os.path.join(sounds_folder, "fredwarn_3.mp3")]
chik_warns = [os.path.join(sounds_folder, "chikwarn_1.mp3"),
              os.path.join(sounds_folder, "chikwarn_2.mp3"),
              os.path.join(sounds_folder, "chikwarn_3.mp3")]

color = "midnightblue"
font = pygame.font.Font('font.otf', 50)
font_time = pygame.font.Font('font.otf', 36)
text1 = font.render("KAMEPЫ", True, color)

clock = pygame.time.Clock()
FPS = 60

cooldown_start_time1 = 0
cooldown_duration1 = 10000
cooldown_start_time2 = 0
cooldown_duration2 = 10000
increment_interval = 60000
count_hour = 0
count_minute = 0
increment_interval_second = 1000
last_time_check = pygame.time.get_ticks()
end_time = time.time() + 360
last_time_check_second = pygame.time.get_ticks()
start_time = pygame.time.get_ticks() + 140300
dor = None

# объявление переменных и загрузка файлов
while True:
    current_time = pygame.time.get_ticks()
    if pygame.time.get_ticks() - last_time_check >= increment_interval:
        count_hour += 1
        last_time_check = pygame.time.get_ticks()

    if pygame.time.get_ticks() - last_time_check_second >= increment_interval_second:
        count_minute += 1
        last_time_check_second = pygame.time.get_ticks()

    if count_minute >= 59:
        count_minute = 0

    if time.time() > end_time:
        pygame.quit()
        sys.exit()
    # кусок кода отвечающий за время
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # событие с появлением

    if current_time - start_time > 0:
        event_interval = random.randint(15000, 26000)
        selected_event = random.choice(["Fredy", "Chika"])
        dor = random.choice(["слева", "справа"])

    # Отрисовка события
        if selected_event == "Fredy" or selected_event == "Chika":
            random_track = random.choice(fred_warns) if selected_event == "Fredy" else random.choice(chik_warns)
            sound = pygame.mixer.Sound(random_track)
            sound.play()

        # Запуск внутреннего таймера на 4 секунды
            inner_timer_start = current_time
            inner_timer_duration = 4000

            while current_time - inner_timer_start < inner_timer_duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Проверка нажатия двери
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if dor == "справа" and 1576 <= mouse_x <= 1678 and 449 <= mouse_y <= 567:
                            # Код, если игрок нажал правую дверь
                            print("Правая дверь нажата!")
                        elif dor == "слева" and 224 <= mouse_x <= 329 and 311 <= mouse_y <= 427:
                            # Код, если игрок нажал левую дверь
                            print("Левая дверь нажата!")

        # Проверка, была ли дверь нажата в течение 4 секунд
            if current_time - inner_timer_start >= inner_timer_duration:
                pass  # Или любой другой код, который вы хотите выполнить после успешного нажатия двери
            else:
                print('gg')
                pygame.quit()  # Вывести "gg", если дверь НЕ была нажата

            sound.stop()
            sound = None

        start_time = current_time + event_interval

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

            if 1576 <= mouse_x <= 1678 and 449 <= mouse_y <= 567:
                if current_time - cooldown_start_time1 >= cooldown_duration1:
                    shock.play(maxtime=0, fade_ms=0)
                    cooldown_start_time1 = current_time
                else:  # код отвечающий за кнопки шока
                    no_energy.play(maxtime=0, fade_ms=0)
            if 224 <= mouse_x <= 329 and 311 <= mouse_y <= 427:
                if current_time - cooldown_start_time2 >= cooldown_duration2:
                    shock.play(maxtime=0, fade_ms=0)
                    cooldown_start_time2 = current_time
                else:
                    no_energy.play(maxtime=0, fade_ms=0)

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(background_image, (screen_width, screen_height)), (0, 0))
    time_text = font_time.render(f"Время: {count_hour}:{str(count_minute).zfill(2)}", True,
                                 (255, 255, 255))  # отображение элементов
    screen.blit(time_text, (screen_width - time_text.get_width() - 90, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
