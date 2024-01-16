import pygame
import sys
import sqlite3

# Инициализация Pygame
pygame.init()

# Разрешение экрана
screen_width = 1920
screen_height = 1080
zapis = pygame.mixer.Sound('music/start_min1.mp3')
# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Миниигра")

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

# Загрузка фоновых изображений и их растягивание
backgrounds = {
    "phonm1": pygame.transform.scale(pygame.image.load("screens/phonm1.jpg"),
                                     (screen_width, screen_height)),
    "police_station": pygame.transform.scale(pygame.image.load("screens/police_station.png"),
                                             (screen_width, screen_height)),
    "wiliam_house": pygame.transform.scale(pygame.image.load("screens/wiliam_house.png"),
                                           (screen_width, screen_height)),
    "afton_house_gg": pygame.transform.scale(pygame.image.load("screens/afton_house_gg.png"),
                                             (screen_width, screen_height))
}

# Загрузка звуков
sounds = {
    "start_min1": pygame.mixer.Sound("music/start_min1.mp3"),
    "police_station_ambient": pygame.mixer.Sound("music/police_station_ambient.mp3"),
    "wiliam_ambient": pygame.mixer.Sound("music/wiliam_ambient.mp3"),
}

# Загрузка текстов
texts_stage2 = [
    "Сейчас допросил работников той пиццерии по делу серии убийств",
    "Указали важную информацию или лицо?",
    "Да, информации я получил много, указали на некого Вильяма Афтона.",
    "Кем он является?",
    "Их конструктор анниматронников.",
    "Нужно допросить его, адрес есть?",
    "Есть",
    "Тогда доставьте его в участок для допроса, действуйте.",
]

texts_stage3 = [
    "Полиция конечно работает оперативно, несомненно...",
    "Чёрт, эти замки заклинило конечно очень сильно...",
    "Надо было наверно почаще их разрабатывать...",
    "Конечно это опасно немного, но что поделаешь...",
    "Да налезай уже... Чёрт, давай же... Наконец то...",
    "Главное тут аккуратность, одно неверное движение и всё...",
]

texts_stage1 = [
    "Спустя неделю после происшествия"
]
played = False
# Инициализация переменных
current_stage = 1
current_text_index = 0
scene4_start_time = 0
# Основной цикл игры
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_stage == 1:
                current_stage = 2
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/police_station_ambient.mp3")
                pygame.mixer.music.play(-1)  # -1 для повторения звука

            elif current_stage == 2:
                if current_text_index < len(texts_stage2) - 1:
                    current_text_index += 1
                else:
                    current_stage = 3
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("music/wiliam_ambient.mp3")
                    pygame.mixer.music.play(-1)
                    current_text_index = 0

            elif current_stage == 3:
                if current_text_index < len(texts_stage3):
                    current_text_index += 1
                else:
                    pygame.mixer.music.load("music/spingrap_gg.mp3")
                    pygame.mixer.music.play()
                    current_stage = 4

    if current_stage == 4:
        if scene4_start_time == 0:
            scene4_start_time = current_time
        elif current_time - scene4_start_time > 10000:  # После 10 секунд
            cur.execute('''UPDATE minigames SET minigame1 = 'unlocked' ''').fetchall()
            con.commit()
            con.close()
            import night_1
            running = False

    # Отрисовка текущего фона
    if current_stage == 1:
        if not played:
            zapis.play()
            played = True
        screen.blit(backgrounds["phonm1"], (0, 0))
        if current_text_index < len(texts_stage1):
            font = pygame.font.Font('font.otf', 50)
            text_surface = font.render(texts_stage1[current_text_index], True, "white")
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface, text_rect)
    elif current_stage == 2:
        screen.blit(backgrounds["police_station"], (0, 0))
        # Отрисовка текстов
        if current_text_index < len(texts_stage2):
            font = pygame.font.Font('font.otf', 37)
            text_surface = font.render(texts_stage2[current_text_index], True, "Blue")
            if current_text_index % 2 == 0:
                screen.blit(text_surface, (0, 300))
            else:
                screen.blit(text_surface, (576, 300))
    elif current_stage == 3:
        screen.blit(backgrounds["wiliam_house"], (0, 0))
        # Отрисовка текстов
        if current_text_index < len(texts_stage3):
            font = pygame.font.Font('font.otf', 50)
            text_surface = font.render(texts_stage3[current_text_index], True, 'Purple')
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface, (75, 900))

    elif current_stage == 4:
        screen.blit(backgrounds["afton_house_gg"], (0, 0))

    print(current_text_index)
    pygame.display.flip()
