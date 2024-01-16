# Катсцены
import pygame
import cv2
# Тимлид:
# В pygame БЫЛ модуль с видео, но к моему ОГРОМНЕЙШЕМУ сожалению, поддержки на него больше нет, поэтому здесь cv2

pygame.mixer.init()
pygame.init()


class Cutscene():
    def __init__(self, video, sound):
        self.video = cv2.VideoCapture(video)  # Сама катсцена
        self.run, self.video_image = self.video.read()  # Запущена ли она или нет; кадр
        self.fps = self.video.get(cv2.CAP_PROP_FPS)  # ФПС
        self.sound = pygame.mixer.music.load(sound)

        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()

    def play_cutscene(self):
        pygame.mixer.music.play()
        run = self.run
        while run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    run = False

            self.run, self.video_image = self.video.read()
            if self.run:
                video_surf = pygame.image.frombuffer(
                    self.video_image.tobytes(), (1920, 1080), "BGR")  # Подрегулированный кадр
            else:
                run = False
            self.screen.blit(video_surf, (0, 0))  # Отображение
            pygame.display.update()
