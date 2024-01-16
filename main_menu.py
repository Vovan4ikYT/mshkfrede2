# Главное меню
import pygame
import sys
import sqlite3
from random import choice
from animation import Animation

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

con = sqlite3.connect('nights.sqlite')
cur = con.cursor()
available_nights = cur.execute('''SELECT night from night_info WHERE unlockation = 'unlocked' ''').fetchall()
# Доступные ночи
current = cur.execute('''SELECT night from night_info WHERE current = 'current' ''').fetchall()
# Текущая ночь
available_nights = [i[0] for i in available_nights]  # Адаптируем под удобный формат
current = [i[0] for i in current]  # Адаптируем под удобный формат

night = current[0]
if night == 5:
    anim = 'springtrap'  # Фон на заднем плане
    color = 'lime'  # Цвет текста
    pygame.mixer.music.load(choice(['music/the_hunt.mp3', 'music/its_me.mp3', 'music/follow_me.mp3', 'music/jaws.mp3']))
    # Музыка
else:
    anim = choice(['freddy', 'baby', 'candy'])
    color = 'deepskyblue'
    pygame.mixer.music.load(choice(['music/mechanical_instinct_ver1.mp3', 'music/mechanical_instinct_ver2.mp3',
                                    'music/we_want_out.mp3']))

images = [pygame.image.load(f'gifs/{anim}/{anim}1.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}2.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}3.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}4.gif'),
          pygame.image.load(f'gifs/{anim}/{anim}5.gif')]  # Изображения в зависимости от anim

gif = Animation(images, 1)  # Анимированный фон
count = 0  # Самый важный параметр, благодаря нему нужным образом отображается текст


class TextLabels():
    def __init__(self):
        self.fonts = [pygame.font.Font('font_main.ttf', 50),
                      pygame.font.Font('font.otf', 50)]  # Шрифты
        self.texts = [self.fonts[0].render('FREDDYS RETURN', True, color),
                      self.fonts[1].render('ЗНАКОМОЕ МЕСТО', True, color),
                      self.fonts[1].render('Выбор ночи', True, color)]
        # Здесь всегда лежат неизменяемые тексты
        self.nights = []  # Ночи
        self.exit_deny = self.fonts[1].render('Выйти', True, 'red')  # Выход/Назад
        self.info = self.fonts[1].render('Об игре', True, color)  # Помощь/Информация
        self.volume = self.fonts[1].render('< ГРОМКОСТЬ >', True, color)  # Громкость музыки в меню

    def text_show(self):
        screen.blit(self.texts[0], (1220, 0))
        screen.blit(self.texts[1], (1220, 70))
        screen.blit(self.exit_deny, (0, 1030))
        screen.blit(self.info, (1220, 1030))
        screen.blit(self.volume, (1220, 890))
        screen.blit(self.texts[2], (1220, 280))
        if count % 2 != 0:  # Только если мы планируем выбирать ночь
            y = 350
            for text in self.nights:
                screen.blit(text, (1220, y))
                y += 70

    def text_change(self):
        if count % 2 != 0:
            self.exit_deny = self.fonts[1].render('Назад', True, 'red')  # Назад
            temp = []  # Доступные ночи
            for night in available_nights:
                temp.append(self.fonts[1].render(f'Ночь {night}', True, color))  # Тексты с ночами
            for i in temp:
                self.nights.append(i)  # Добавляем доступные ночи
        else:
            self.nights.clear()
            self.exit_deny = self.fonts[1].render('Выйти', True, 'red')  # Выйти

    def start_play_night(self):
        if count % 2 != 0 and pygame.mouse.get_pos()[0] in range(1220, 1520):
            if pygame.mouse.get_pos()[1] in range(350, 400) and 1 in available_nights:
                with open('current_night.txt', 'w') as f_cur:
                    f_cur.write('1')
            elif pygame.mouse.get_pos()[1] in range(420, 470) and 2 in available_nights:
                with open('current_night.txt', 'w') as f_cur:
                    f_cur.write('2')
            elif pygame.mouse.get_pos()[1] in range(490, 540) and 3 in available_nights:
                with open('current_night.txt', 'w') as f_cur:
                    f_cur.write('3')
            elif pygame.mouse.get_pos()[1] in range(560, 610) and 4 in available_nights:
                with open('current_night.txt', 'w') as f_cur:
                    f_cur.write('4')
            elif pygame.mouse.get_pos()[1] in range(630, 680) and 5 in available_nights:
                with open('current_night.txt', 'w') as f_cur:
                    f_cur.write('5')
            con.close()
            import start_night
            pygame.quit()
            sys.exit()


pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

text_labels = TextLabels()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            text_labels.start_play_night()
            if event.pos[0] in range(1220, 1520) and event.pos[1] in range(280, 350):
                if count % 2 == 0:
                    count += 1
                    text_labels.text_change()  # Выбор ночи
            elif event.pos[0] in range(0, 250) and event.pos[1] in range(1030, 1080):
                if count % 2 == 0:
                    sys.exit()  # Выход
                else:
                    count -= 1
                    text_labels.text_change()  # Назад
            elif event.pos[0] in range(1220, 1270) and event.pos[1] in range(890, 940):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)  # -громкость
            elif event.pos[0] in range(1620, 1770) and event.pos[1] in range(890, 940):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)  # +громкость
            elif event.pos[0] in range(1220, 1570) and event.pos[1] in range(1030, 1080):
                con.close()
                import information_menu  # Об игре
                sys.exit()
    clock.tick(60)
    move = choice(range(0, 100))  # Счётчик, обеспечивающий типо "глючную" анимацию
    if move <= 5:
        gif.change(10)  # Смена картинки на фоне
        screen.blit(gif.image, (0, 0))  # Отображение фона
        text_labels.text_show()  # Отображение текста
    pygame.display.update()
