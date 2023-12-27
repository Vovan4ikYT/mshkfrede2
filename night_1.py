# 1 ночь
import pygame
import sys

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.music.load('music/night1amb.mp3')
sound = pygame.mixer.Sound('sounds/shock.mp3')

background_image = pygame.image.load("ofices/ofice1_night1.png").convert()
pygame.mixer.music.play(-1)

color = "midnightblue"
font = pygame.font.Font('font.otf', 50)
text1 = font.render("KAMEPЫ", True, color)
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if 1576 <= mouse_x <= 1678 and 449 <= mouse_y <= 567:
                sound.play(maxtime=0, fade_ms=0)
                # Кнопки
            if 224 <= mouse_x <= 329 and 311 <= mouse_y <= 427:
                sound.play(maxtime=0, fade_ms=0)

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(background_image, (screen_width, screen_height)), (0, 0))
    rect = pygame.draw.rect(screen, color, (680, 915, 600, 120), border_radius=30, width=5)

    screen.blit(text1, (860, 950))
    if 667 <= mouse_x <= 1276 and 918 <= mouse_y <= 12294:
        pass
        # Наработка открытия камер
    pygame.display.flip()