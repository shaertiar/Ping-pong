import pygame as pg
import settings

# Класс игрока
class Player:
    # Конструктор
    def __init__(self, window, color:tuple, y:int, buttons:tuple, speed:int):
        self.window = window
        self.color = color
        self.width = 100
        self.spawn_x = (settings.ww - self.width)/2
        self.rect = pg.rect.Rect(self.spawn_x, y, self.width, 10)
        self.button_left = buttons[0]
        self.button_right = buttons[1]
        self.speed = speed
        self.points = 0

    # Функция для обновления
    def update(self):
        # Увеличение скорости
        self.speed += 0.1/24

        # Обработка нажатий
        keys = pg.key.get_pressed()

        if keys[self.button_left]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

        elif keys[self.button_right]:
            if self.rect.x + self.rect.width < settings.ww:
                self.rect.x += self.speed

    # Функция для отрисовки
    def draw(self):
        pg.draw.rect(self.window, self.color, self.rect)

    # Функция для перемещения игрока на изначальное место
    def restart(self):
        self.spawn_x = (settings.ww - self.width)/2
        self.rect.x = self.spawn_x