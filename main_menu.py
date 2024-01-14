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
con.close()
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
        # Здесь всегда лежат неизменяемые тексты, и по ситуации тексты с ночами
        self.exit_deny = self.fonts[1].render('Выйти', True, 'red')  # Выход/Назад
        self.help, self.info = (self.fonts[1].render('Инструкция', True, color),
                                self.fonts[1].render('Об игре', True, color))  # Помощь/Информация
        self.continue_night = self.fonts[1].render(f'Продолжить: Ночь {current[0]}', True, color)
        # Продолжить ночь
        self.volume = self.fonts[1].render('< ГРОМКОСТЬ >', True, color)  # Громкость музыки в меню

    def text_show(self):
        screen.blit(self.texts[0], (1220, 0))
        screen.blit(self.texts[1], (1220, 70))
        screen.blit(self.exit_deny, (0, 1030))
        screen.blit(self.help, (1220, 960))
        screen.blit(self.info, (1220, 1030))
        screen.blit(self.continue_night, (1220, 820))
        screen.blit(self.volume, (1220, 890))
        screen.blit(self.texts[2], (1220, 280))
        if count % 2 != 0:  # Только если мы планируем выбирать ночь
            y = 350
            for text in self.texts[3:]:
                screen.blit(text, (1220, y))
                y += 70

    def text_change(self):
        if count % 2 != 0:
            self.exit_deny = self.fonts[1].render('Назад', True, 'red')  # Назад
            temp = []  # Доступные ночи
            for night in available_nights:
                temp.append(self.fonts[1].render(f'Ночь {night}', True, color))  # Тексты с ночами
            for i in temp:
                self.texts.append(i)  # Добавляем доступные ночи
        else:
            for i in range(len(self.texts)):
                if i != 0 and i != 1 and i != 2:  # Нужно, чтобы не пропали неизменяемые тексты
                    self.texts.remove(self.texts[i])  # Удаляем доступные ночи
            self.exit_deny = self.fonts[1].render('Выйти', True, 'red')  # Выйти


pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

text_labels = TextLabels()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
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
    clock.tick(60)
    move = choice(range(0, 100))  # Счётчик, обеспечивающий типо "глючную" анимацию
    if move <= 5:
        gif.change(10)  # Смена картинки на фоне
        screen.blit(gif.image, (0, 0))  # Отображение фона
        text_labels.text_show()  # Отображение текста
    pygame.display.update()
