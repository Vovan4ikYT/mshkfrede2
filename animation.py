from pygame import *

# Тимлид: К большому сожалению, код был найден в Интернете. Но разобравшись в нём и поняв, как он работает,
# я понял, что работает он отлично


class Animation(sprite.Sprite):
    def __init__(self, images, time_interval):
        super(Animation, self).__init__()
        self.images = images  # Список изображений
        self.image = self.images[0]  # Текущее изображение
        self.time_interval = time_interval  # Скорость протекания
        self.index = 0  # Индекс текущего изображения
        self.timer = 0  # Счётчик протекания

    def change(self, seconds):
        self.timer += seconds  # second - скорость протекания
        if self.timer >= self.time_interval:

            # Смена изображения
            self.image = self.images[self.index]
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0
            