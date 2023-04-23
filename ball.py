import pygame as pg
import settings
import random

# Класс мяча
class Ball:
    # Конструктор
    def __init__(self, window, side:int, x:int, y:int, speed:int):
        self.window = window
        self.color = (255, 255, 255)
        self.rect = pg.rect.Rect(x, y, side, side)
        self.speed = speed
        self.is_down = random.choice([True, False])
        self.is_right = random.choice([True, False])

    # Метод для обновления
    def update(self):
        # Движение по вертикали
        if self.is_down:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

        # Движение по горизонтали
        if self.is_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Изменение направления по горизонтали
        if self.rect.x + self.rect.width >= settings.ww:
            self.is_right = False
            self.speed += 0.1
        elif self.rect.x <= 0:
            self.is_right = True
            self.speed += 0.1

    # Функция для отрисовки
    def draw(self):
        pg.draw.rect(self.window, self.color, self.rect)

    # Функция для возвращения мяча на исходное место
    def restart(self):
        self.rect.x, self.rect.y = 240, 240
        self.is_down = random.choice([True, False])
        self.is_right = random.choice([True, False])
