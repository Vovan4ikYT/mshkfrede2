# Анимация

from pygame import *


class Animation(sprite.Sprite):
    def __init__(self, images, time_interval):
        super(Animation, self).__init__()
        self.images = images
        self.image = self.images[0]
        self.time_interval = time_interval
        self.index = 0
        self.timer = 0

    def change(self, seconds):
        self.timer += seconds
        if self.timer >= self.time_interval:
            self.image = self.images[self.index]
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0