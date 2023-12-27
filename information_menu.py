# Меню с информацией об игре

import pygame
import sys
import subprocess

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

pygame.mixer.music.load('music/real_ambient.mp3')

back_image = pygame.image.load('ofices/office2.png').convert()

background_image = pygame.transform.scale(back_image, (1920, 1080))

color = "Brown"

txt1 = 'Вы - Джереми Шмидт. Вы имели дело с Fazber Entertainment'
txt2 = 'и знаете про неё всё. Эта организация - скрывает многое.'
txt3 = 'Ранее вы уже боролись с ней. В последний раз, вы нанесли'
txt4 = 'сокрушительный удар, заставив организацию ненадолго'
txt5 = 'прекратить свои зверства. Но ничто не длиться вечно.'
txt6 = 'Они снова готовы творить ужасные дела руками своих'
txt7 = 'аниматронных машин. Они открывают новое заведение. Вы'
txt8 = 'намеренны довести дело до конца и устраивайтесь к ним'
txt9 = 'на работу, что вы воплотить свои планы.'


font1, font2 = pygame.font.Font('font_main.ttf', 50), pygame.font.Font('font.otf', 50)
text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14 = (
    font1.render('FREDDYS RETURN', True, color),
    font2.render('ЗНАКОМОЕ МЕСТО', True, color),
    font2.render('Назад', True, color),
    font2.render('< ГРОМКОСТЬ >', True, color),
    font2.render(txt1, True, color),
    font2.render(txt2, True, color),
    font2.render(txt3, True, color),
    font2.render(txt4, True, color),
    font2.render(txt5, True, color),
    font2.render(txt6, True, color),
    font2.render(txt7, True, color),
    font2.render(txt8, True, color),
    font2.render(txt9, True, color),
    font2.render('Предыдущая игра', True, color))

pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            print(i.pos)
            if i.pos[0] in range(0, 190) and i.pos[1] in range(1030, 1080):
                sys.exit()
            elif i.pos[0] in range(1485, 1515) and i.pos[1] in range(795, 845):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
            elif i.pos[0] in range(1885, 1915) and i.pos[1] in range(795, 845):
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
            elif i.pos[0] in range(676, 1240) and i.pos[1] in range(910, 931):
                subprocess.run(["start", "https://github.com/Vovan4ikYT/frede"], shell=True)

    clock.tick(60)
    screen.blit(text1, (650, 100))
    screen.blit(text2, (680, 200))
    screen.blit(text3, (0, 1030))
    screen.blit(text4, (1490, 800))
    screen.blit(text5, (0, 300))
    screen.blit(text6, (0, 350))
    screen.blit(text7, (0, 400))
    screen.blit(text8, (0, 450))
    screen.blit(text9, (0, 500))
    screen.blit(text10, (0, 550))
    screen.blit(text11, (0, 600))
    screen.blit(text12, (0, 650))
    screen.blit(text13, (0, 700))
    screen.blit(text14, (680, 900))

    pygame.display.flip()
    screen.blit(back_image, (0, 0))
