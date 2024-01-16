import pygame
import sys
import sqlite3
from animation import Animation
from cutscene import Cutscene
from jumpscares import candy, popgoes

pygame.mixer.init(channels=4)
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# Картинки
service = pygame.image.load('parts_and_service.jpg')
tape_player = pygame.image.load('tape.png')
repair_surfs = [pygame.image.load('gifs/candy/repair/candy1.png'),
                pygame.image.load('gifs/candy/repair/candy2.png'),
                pygame.image.load('gifs/candy/repair/candy1_repair.png'),
                pygame.image.load('gifs/candy/repair/candy2_repair.png')]
popgoes_surfs = [pygame.image.load('gifs/popgoes/popgoes1.png'),
                 pygame.image.load('gifs/popgoes/popgoes2.png')]
cur_candy = repair_surfs[0]
cur_popgoes = popgoes_surfs[0]

# БД
con = sqlite3.connect('nights.sqlite')
cur = con.cursor()

cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '3' ''').fetchall()  # Текущая ночь
cur.execute('''UPDATE night_info SET current = NULL WHERE night NOT LIKE '3' ''').fetchall()  # Остальные не текущие
con.commit()

# Плеер
music_tape = None
music_tape_candy = pygame.mixer.Sound('sounds/candy_tape.mp3')
music_tape_popgoes = pygame.mixer.Sound('sounds/popgoes_tape.mp3')

zapis = pygame.mixer.Sound('sounds/nightfm3.mp3')
pygame.mixer.Channel(3).play(zapis)

tool = False

candy_gif = Animation(candy, time_interval=26)
candy_count = 350
candy_state = 'idle'

popgoes_gif = Animation(popgoes, time_interval=6)
popgoes_count = 350
halun = Animation([pygame.image.load('gifs/popgoes/halun/halun1.png'),
                   pygame.image.load('gifs/popgoes/halun/halun2.png'),
                   pygame.image.load('gifs/popgoes/halun/halun3.png')], time_interval=3)

# Ящик
repair_details = [pygame.image.load('gifs/candy/repair/repair_right_leg.png'),
                  pygame.image.load('gifs/candy/repair/repair_left_leg.png'),
                  pygame.image.load('gifs/candy/repair/repair_battery.png')]
box = pygame.image.load('gifs/candy/repair/repair_box.png')
tool_surf = pygame.image.load('gifs/candy/repair/repair_tool.png')
current_detail = pygame.image.load('gifs/candy/repair/repair_tool.png')
left_count, right_count, battery_count = 0, 0, 0
repaired = 0

cutscene_night3 = Cutscene('cutscenes/cutscene_night3.mp4', 'sounds/cutscenes/cutscene_night3.mp3')


def candy_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    # Так звук красивее проигрывается

    scream = pygame.mixer.Sound('sounds/jumpscares/candy_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(676):
        candy_gif.change(1)
        screen.blit(candy_gif.image, (0, 0))
        pygame.display.update()
    con.close()
    import lose
    sys.exit()


def popgoes_death():
    for channel in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(channel).stop()
    scream = pygame.mixer.Sound('sounds/jumpscares/popgoes_jumpscare.mp3')
    pygame.mixer.Channel(0).play(scream)
    for i in range(36):
        screen.fill((0, 0, 0))
        popgoes_gif.change(1)
        screen.blit(popgoes_gif.image, (0, 0))
        pygame.display.update()
    con.close()
    import lose
    sys.exit()


def repair_box():
    global box, candy_state
    if candy_state == 'repair':
        box = pygame.image.load('gifs/candy/repair/repair_box_open.png')
        x = 614
        for i in range(len(repair_details)):
            screen.blit(repair_details[i], (x, 817))
            x += 88
        pygame.display.update()


# Ремонт
def repairing():
    global left_count, right_count, battery_count, candy_state
    if candy_state == 'repair':
        if ((pygame.mouse.get_pos()[0] in range(614, 702) and pygame.mouse.get_pos()[1] in range(817, 842)) or
                (pygame.mouse.get_pos()[0] in range(1191, 1211) and pygame.mouse.get_pos()[1] in range(803, 822))):
            right_count += 1
        elif ((pygame.mouse.get_pos()[0] in range(1253, 1272) and pygame.mouse.get_pos()[1] in range(806, 821)) or
                (pygame.mouse.get_pos()[0] in range(702, 790) and pygame.mouse.get_pos()[1] in range(817, 842))):
            left_count += 1
        elif ((pygame.mouse.get_pos()[0] in range(790, 862) and pygame.mouse.get_pos()[1] in range(817, 844)) or
                (pygame.mouse.get_pos()[0] in range(1298, 1324) and pygame.mouse.get_pos()[1] in range(704, 817))):
            battery_count += 1


# Проверка деталей
def check_detail():
    global candy_state, left_count, right_count, battery_count
    # У каждой детали есть свой счётчик готовности

    if candy_state == 'repair':
        if right_count == 2:
            detail = pygame.transform.rotate(repair_details[0], 90)
            screen.blit(detail, (1191, 803))
        if left_count == 2:
            detail = pygame.transform.rotate(repair_details[1], 90)
            screen.blit(detail, (1253, 806))
        if battery_count == 2:
            detail = pygame.transform.scale(repair_details[2], (45, 27))
            detail = pygame.transform.rotate(detail, 15)
            screen.blit(detail, (1288, 694))


while True:
    # Победа
    if repaired == 99:
        for channel in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(channel).stop()
        cur.execute('''UPDATE night_info SET unlockation = 'unlocked' WHERE night = '4' ''').fetchall()
        cur.execute('''UPDATE night_info SET current = 'current' WHERE night = '4' ''').fetchall()  # Текущая ночь
        cur.execute(
            '''UPDATE night_info SET current = NULL WHERE night NOT LIKE '4' ''').fetchall()  # Остальные не текущие
        con.commit()
        con.close()
        cutscene_night3.play_cutscene()
        sys.exit()

    # Плеер
    if pygame.mixer.Channel(1).get_busy() is True:
        if music_tape == music_tape_candy:
            candy_count += 1
            popgoes_count -= 1
        if music_tape == music_tape_popgoes:
            popgoes_count += 1
            candy_count -= 1
    else:
        candy_count -= 1
        popgoes_count -= 1

    # Кэнди
    if candy_count <= 200:
        if left_count != 3:
            left_count = 0
        if right_count != 3:
            right_count = 0
        if battery_count != 3:
            battery_count = 0
        tool = False
        repaired = 0
        if candy_count == 0:
            candy_death()
        else:
            if candy_state == 'idle':
                cur_candy = repair_surfs[1]
            elif candy_state == 'repair':
                cur_candy = repair_surfs[3]
    elif candy_count > 200:
        if candy_count >= 350:
            pygame.mixer.Channel(1).stop()
        if candy_state == 'idle':
            cur_candy = repair_surfs[0]
        elif candy_state == 'repair':
            cur_candy = repair_surfs[2]

    # Попгоус
    if popgoes_count <= 200:
        if popgoes_count == 0:
            popgoes_death()
        else:
            cur_popgoes = popgoes_surfs[1]
            halun.change(1)
            screen.blit(halun.image, (0, 0))
            pygame.display.update()
    elif popgoes_count > 200:
        if popgoes_count >= 350:
            pygame.mixer.Channel(1).stop()
        cur_popgoes = popgoes_surfs[0]

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

            # Начало ремонта
            if event.pos[0] in range(1266, 1301) and event.pos[1] in range(500, 516) and candy_state == 'idle':
                nos = pygame.mixer.Sound('sounds/nos_cende.mp3')
                pygame.mixer.Channel(2).play(nos)
                candy_state = 'repair'

            # Плеер Кэнди
            if event.pos[0] in range(1828, 1863) and event.pos[1] in range(869, 896):
                music_tape = music_tape_candy
                pygame.mixer.Channel(1).play(music_tape)

            # Плеер Попгоуса
            if event.pos[0] in range(1859, 1898) and event.pos[1] in range(869, 896):
                music_tape = music_tape_popgoes
                pygame.mixer.Channel(1).play(music_tape)

            # Инструмент
            if event.pos[0] in range(508, 547) and event.pos[1] in range(824, 880):
                tool = True
            if event.pos[0] in range(1843, 1867) and event.pos[1] in range(694, 717):
                # Миниигра
                for channel in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(channel).stop()
                con.close()
                import minigame_3

            # Использование инструмента
            if event.pos[0] in range(1208, 1232) and event.pos[1] in range(667, 685) and tool is True:
                if left_count == 2 and right_count == 2 and battery_count == 2:
                    tool_sound = pygame.mixer.Sound('sounds/tool.mp3')
                    pygame.mixer.Channel(2).play(tool_sound)
                    repaired += 33
            repairing()

    screen.fill((0, 0, 0))
    screen.blit(service, (0, 0))
    screen.blit(cur_candy, (900, 300))
    screen.blit(tape_player, (1565, 620))
    screen.blit(box, (579, 737))
    screen.blit(tool_surf, (479, 807))
    screen.blit(cur_popgoes, (-100, 300))
    repair_box()
    check_detail()
    pygame.display.update()