import pygame as pg
import settings

# Класс Бота
class Bot:
    # Конструктор
    def __init__(self, window, color:tuple, y:int, ball, speed:int):
        self.window = window
        self.color = color
        self.width = 100
        self.spawn_x = (settings.ww - self.width)/2
        self.rect = pg.rect.Rect(self.spawn_x, y, self.width, 10)
        self.ball = ball
        self.speed = speed
        self.points = 0

    # Функция обновления
    def update(self):
        if self.ball.rect.x + self.ball.rect.width / 2 > self.rect.x + self.rect.width / 2:
            if self.rect.x + self.rect.width <= settings.ww:
                self.rect.x += self.speed

        elif self.ball.rect.x + self.ball.rect.width / 2 < self.rect.x + self.rect.width / 2:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    # Функцция для отрисовки
    def draw(self):
        pg.draw.rect(self.window, self.color, self.rect)

    # Функция для перемещения бота на изночальное место
    def restart(self):
        self.spawn_x = (settings.ww - self.width)/2
        self.rect.x = self.spawn_x
