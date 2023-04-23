import pygame as pg

import settings
import player
import bot
import ball

import time

# Иниацилизация 
pg.init()

# Создание часов
clock = pg.time.Clock()

# Создание шрифта
my_font = pg.font.SysFont('arial', 45)
my_font_small = pg.font.SysFont('arial', 30)

# Создание окна
window = pg.display.set_mode((settings.ww, settings.wh))
pg.display.set_caption('Пинг-Понг')

# Создание мяча
my_ball = ball.Ball(window, 20, (settings.ww-20)/2, (settings.wh-20)/2, 6)

# Цикл приложения
is_app = True
while is_app:
    # Создание переменной с режимом игры
    play_mode = 0

    # Создание переменной с позицией мышки
    mouse_pos = (10000, 10000)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            is_app = False

        # Обработка нажатий мышки
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

    # Окрашивание экрана
    window.fill((0, 0, 0))

    # Отрисовка текста
    text = my_font.render('Выберите режим игры', False, (255, 255, 255))
    window.blit(text, ((settings.ww - text.get_width())/2, 0))

    # Кнопка игры с ботом
    button1 = my_font_small.render('С ботом', False, (255, 255, 255), (123, 123, 123))
    button1_rect = button1.get_rect()
    button1_rect.x = settings.ww / 4 - button1_rect.width / 2
    button1_rect.y = settings.wh / 2 - button1_rect.height / 2
    window.blit(button1, (button1_rect.x, button1_rect.y))
    
    # Кнопка игры с другом
    button2 = my_font_small.render('С другом', False, (255, 255, 255), (123, 123, 123))
    button2_rect = button2.get_rect()
    button2_rect.x = settings.ww / 4 * 3 - button2_rect.width / 2
    button2_rect.y = settings.wh / 2 - button2_rect.height / 2
    window.blit(button2, (button2_rect.x, button2_rect.y))


    # Проверка нажатий на кнопки
    if button1_rect.collidepoint(mouse_pos):
        play_mode = 1
        
        # Создание игроков
        player1 = player.Player(window, (255, 0, 0), 10, (pg.K_LEFT, pg.K_RIGHT), 5)
        player2 = bot.Bot(window, (0, 0, 255), 480, my_ball, 6)

        mouse_pos = (0, 0)

    elif button2_rect.collidepoint(mouse_pos):
        play_mode = 2
        
        # Создание игроков
        player1 = player.Player(window, (255, 0, 0), 10, (pg.K_LEFT, pg.K_RIGHT), 5)
        player2 = player.Player(window, (0, 0, 255), 480, (pg.K_a, pg.K_d), 5)

        mouse_pos = (0, 0)

    # Начатие игры
    if play_mode != 0:
        # Цикл игры
        is_game = True
        while is_game:
            is_continue = True

            # Рестарт игроков
            player1.restart()
            player2.restart()

            # Рестарт мяча
            my_ball.restart()

            # Цикл раунда
            is_round = True
            while is_round: 
                # Обработка событий
                for event in pg.event.get():
                    # Выход
                    if event.type == pg.QUIT:
                        is_app = False
                        is_game = False
                        is_round = False

                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            is_game = False
                            is_round = False
                            play_mode = 0
                            my_ball = ball.Ball(window, 20, (settings.ww-20)/2, (settings.wh-20)/2, 6)

                # Закрашвание окна
                window.fill((0, 0, 0))

                # Отрисовка очков
                score = my_font.render(f'{player1.points} : {player2.points}', False, (123, 123, 123))
                window.blit(score, ((settings.ww - score.get_width())/2, (settings.wh - score.get_height())/2))

                # Обновление и ототрисовка игроков
                player1.update()
                player2.update()
                player1.draw()
                player2.draw()

                if is_continue:
                    # Обновление и отричовка игроков
                    my_ball.update()
                    my_ball.draw()

                    # Проверка столкновений мяча с игроками
                    if pg.sprite.collide_rect(my_ball, player1):
                        my_ball.is_down = True
                        my_ball.color = (200, 0, 0)

                    elif pg.sprite.collide_rect(my_ball, player2):
                        my_ball.is_down = False
                        my_ball.color = (0, 0, 200)

                    # Проверка количества очков у игроков
                    if player1.points >= 7:
                        player1.points = 'WIN'
                        player2.points = 'Lose'

                        is_continue = False

                    elif player2.points >= 7:
                        player1.points = 'WIN'
                        player2.points = 'Lose'

                        is_continue = False

                    # Проверка вылета мяча за поле
                    if my_ball.rect.y <= 10:
                        player2.points += 1

                        is_round = False

                        # Окрашивание экрана
                        window.fill((0, 0, 0))

                    elif my_ball.rect.y + my_ball.rect.height >= settings.wh - 10:
                        player1.points += 1

                        is_round = False

                        # Окрашивание экрана
                        window.fill((0, 0, 0))

                # Обновление окна
                pg.display.update()
                clock.tick(settings.fps)

            # 1 сек
            if is_round:
                time.sleep(1)

    # Обновление окна
    pg.display.update()
    clock.tick(settings.fps)