import pygame
import sys

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))

with open('current_night.txt', encoding='utf-8') as f:
    number = f.readlines()  # Запущенная ночь

if number[0] == '5':
    pygame.mixer.music.load('sounds/start_night5.mp3')  # Звук старта ночи
    color = 'green'  # Цвет текста
else:
    pygame.mixer.music.load('sounds/start_night.mp3')
    color = 'white'

with open(f'{number[0]}_guide.txt', encoding='utf-8') as file:
    lines = file.readlines()  # Нужная нам инструкция

font = pygame.font.Font('font.otf', 30)
y = 0

pygame.mixer.music.play()

screen.fill((0, 0, 0))

# Отображение текста
for i in range(len(lines)):
    screen.blit(font.render(lines[i].rstrip('\n'), True, color), (500, y))
    y += 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:

            # Запуск ночи
            if number[0] == '1':
                import night_1
            elif number[0] == '2':
                import night_2
            elif number[0] == '3':
                import night3
            elif number[0] == '4':
                import night4
            elif number[0] == '5':
                import night5
    pygame.display.update()
