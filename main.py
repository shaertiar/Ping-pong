import pygame as pg
import random 
import time

# Иниацилизация 
pg.init()

# Настройки окна
ww, wh = 500, 500
fps = 60

# Класс игрока
class Player:
    # Конструктор
    def __init__(self, color:tuple, y:int, buttons:tuple, speed:int):
        self.color = color
        self.width = 100
        self.spawn_x = (ww - self.width)/2
        self.rect = pg.rect.Rect(self.spawn_x, y, self.width, 10)
        self.button_left = buttons[0]
        self.button_right = buttons[1]
        self.speed = speed
        self.points = 0

    # Функция для обновления
    def update(self):
        keys = pg.key.get_pressed()

        if keys[self.button_left]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

        elif keys[self.button_right]:
            if self.rect.x + self.rect.width < ww:
                self.rect.x += self.speed

    # Функция для отрисовки
    def draw(self):
        pg.draw.rect(window, self.color, self.rect)

    # Функция для перемещения игрока на изначальное место
    def restart(self):
        self.spawn_x = (ww - self.width)/2
        self.rect.x = self.spawn_x

# Класс мяча
class Ball:
    # Конструктор
    def __init__(self, side:int, x:int, y:int, speed:int):
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
        if self.rect.x + self.rect.width >= ww:
            self.is_right = False
            self.speed += 0.1
        elif self.rect.x <= 0:
            self.is_right = True
            self.speed += 0.1

    # Функция для отрисовки
    def draw(self):
        pg.draw.rect(window, self.color, self.rect)

# Создание часов
clock = pg.time.Clock()

# Создание шрифта
my_font = pg.font.SysFont('serif', 50)

# Создание окна
window = pg.display.set_mode((ww, wh))
pg.display.set_caption('Пинг-Понг')

# Создание игроков
player1 = Player((255, 0, 0), 10, (pg.K_LEFT, pg.K_RIGHT), 2)
player2 = Player((0, 0, 255), 480, (pg.K_a, pg.K_d), 2)

# Цикл приложения
is_app = True
while is_app:
    is_continue = True

    # Рестарт игроков
    player1.restart()
    player2.restart()

    # Создание мяча
    ball = Ball(20, 240, 240, 1)

    # Игровой цикл
    is_game = True
    while is_game:
        # Обработка событий
        for event in pg.event.get():
            # Выход
            if event.type == pg.QUIT:
                is_game = False
                is_app = False

        # Закрашвание окна
        window.fill((0, 0, 0))

        # Отрисовка очков
        score = my_font.render(f'{player1.points} : {player2.points}', False, (123, 123, 123))
        window.blit(score, ((ww - score.get_width())/2, (wh - score.get_height())/2))

        # Обновление и ототрисовка игроков
        player1.update()
        player2.update()
        player1.draw()
        player2.draw()

        if is_continue:
            # Обновление и отричовка игроков
            ball.update()
            ball.draw()

            # Проверка столкновений мяча с игроками
            if pg.sprite.collide_rect(ball, player1):
                ball.is_down = True
                ball.color = (200, 0, 0)

            elif pg.sprite.collide_rect(ball, player2):
                ball.is_down = False
                ball.color = (0, 0, 200)

            # Проверка количества очков у игроков
            if player1.points >= 5:
                player1.points = 'WIN'
                player2.points = 'Lose'

                is_continue = False

            elif player2.points >= 5:
                player1.points = 'WIN'
                player2.points = 'Lose'

                is_continue = False

            # Проверка вылета мяча за поле
            if ball.rect.y <= 10:
                player2.points += 1

                is_game = False
                
                # Окрашивание экрана
                window.fill((0, 0, 0))

            elif ball.rect.y + ball.rect.height >= wh - 10:
                player1.points += 1

                is_game = False

                # Окрашивание экрана
                window.fill((0, 0, 0))

        # Обновление окна
        pg.display.update()
        clock.tick(fps)
        
    # Окрашивание экрана
    window.fill((0, 0, 0))

    # 1 сек
    if is_app:
        time.sleep(1)