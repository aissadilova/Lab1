import pygame
import random
import sys
import psycopg2
from pygame import time
# подключаемся к базе данных
connection = psycopg2.connect(dbname="snakegame", user="postgres", password="postgres", host="localhost")  # устанавливаем соединение с PostgreSQL
connecttobaza = connection.cursor()  # создаем объект для выполнения SQL-запросов

# создание таблицы пользователей, если она не существует
connecttobaza.execute(
    'CREATE TABLE IF NOT EXISTS users('  # запрос на создание таблицы пользователей
    'id SERIAL PRIMARY KEY, '  # поле id будет уникальным идентификатором
    'username TEXT UNIQUE'  # имя пользователя должно быть уникальным
    ')'
)
connection.commit()  # применяем изменения в базе данных

# создание таблицы для хранения очков пользователей, если она не существует
connecttobaza.execute(
    'CREATE TABLE IF NOT EXISTS user_score('  # запрос на создание таблицы очков
    'id SERIAL PRIMARY KEY, '  # поле id для уникальности
    'user_id INTEGER, '  # поле для хранения id пользователя
    'level INTEGER, '  # поле для хранения уровня игрока
    'score INTEGER, '  # поле для хранения очков игрока
    'FOREIGN KEY(user_id) REFERENCES users(id) '  # связь с таблицей users через user_id
    ')'
)
connection.commit()  # применяем изменения в базе данных

# настройки
SCREEN_WIDTH = 600  # ширина экрана игры
SCREEN_HEIGHT = 400  # высота экрана игры
CELL_SIZE = 20  # размер ячеек, в которых будет двигаться змейка
FPS = 8  # начальная скорость игры

# цвета
BLACK = (0, 0, 0)  # черный цвет для фона
RED = (255, 0, 0)  # красный для головы змейки
GREEN = (0, 255, 0)  # зеленый для обычной еды
YELLOW = (255, 255, 0)  # желтый для тела змейки
BLUE = (0, 0, 255)  # синий для специальной еды
PURPLE = (128, 0, 128)  # фиолетовый для ценной еды
WHITE = (255, 255, 255)  # белый цвет для текста

# класс для хранения координат x и y
class Point:
    def __init__(self, x, y):
        self.x = x  # координата x
        self.y = y  # координата y

# класс змейки с логикой управления и отрисовки
class Snake:
    def __init__(self):
        self.body = [Point(5, 5), Point(4, 5), Point(3, 5)]  # начальная позиция змейки
        self.dx, self.dy = 1, 0  # направление змейки (вправо)
        self.score = 0  # начальные очки
        self.speed = 2  # начальная скорость змейки
        self.level = 1  # начальный уровень
        self.walls = []  # список стен, которые будут добавлены в уровне

    # функция для перемещения змейки
    def move(self):
        for i in range(len(self.body)-1, 0, -1):  # сдвигаем каждый сегмент тела змейки
            self.body[i].x = self.body[i-1].x  # перемещаем сегменты
            self.body[i].y = self.body[i-1].y  # перемещаем сегменты
        self.body[0].x += self.dx  # перемещаем голову змейки по оси x
        self.body[0].y += self.dy  # перемещаем голову змейки по оси y

    # функция для отрисовки змейки
    def draw(self):
        for segment in self.body[1:]:  # отрисовываем тело змейки
            pygame.draw.rect(screen, YELLOW, 
                            (segment.x*CELL_SIZE, segment.y*CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, 
                        (self.body[0].x*CELL_SIZE, self.body[0].y*CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))  # отрисовываем голову змейки
    
    # функция для увеличения змейки
    def grow(self, amount=1):
        for _ in range(amount):  # добавляем новые сегменты тела змейки
            tail = self.body[-1]  # берем последний сегмент змейки
            self.body.append(Point(tail.x, tail.y))  # добавляем новый сегмент
    
    # изменение направления движения
    def change_direction(self, new_dx, new_dy):
        if (self.dx * new_dx == 0) and (self.dy * new_dy == 0):  # проверка, чтобы нельзя было двигаться в противоположную сторону
            self.dx, self.dy = new_dx, new_dy  # обновляем направление змейки

    # увеличение уровня
    def increase_level(self):
        if self.score >= self.level * 10:  # уровень увеличивается каждые 10 очков
            self.level += 1  # увеличиваем уровень
            self.speed += 1  # увеличиваем скорость на каждом уровне
            self.create_walls()  # создаем новые стены для следующего уровня

    # генерация стен для нового уровня
    def create_walls(self):
        self.walls = []  # очищаем старые стены
        if self.level == 2:
            self.walls = [Point(10, 5), Point(11, 5), Point(12, 5)]  # пример стены для уровня 2
        elif self.level == 3:
            self.walls = [Point(8, 3), Point(9, 3), Point(10, 3), Point(11, 3)]  # пример стены для уровня 3

    # сохранение текущего счета в базу данных
    def save_score_to_db(self, user_id):
        connecttobaza.execute(
            'INSERT INTO user_score (user_id, level, score) '
            'VALUES (%s, %s, %s)', (user_id, self.level, self.score)  # записываем очки и уровень в базу
        )
        connection.commit()  # применяем изменения в базе данных

# класс еды с разными типами
class Food:
    def __init__(self):
        self.types = [
            {"color": GREEN, "weight": 1, "lifetime": None},  # обычная еда
            {"color": BLUE, "weight": 2, "lifetime": 5000},   # временная еда (5 сек)
            {"color": PURPLE, "weight": 3, "lifetime": 3000}  # ценная еда (3 сек)
        ]
        self.current_food = self.generate_food()  # генерируем начальную еду
        
    # генерация случайной еды
    def generate_food(self):
        food_type = random.choices(
            self.types, 
            weights=[70, 20, 10],  # вероятности появления разных типов еды
            k=1
        )[0]
        
        return {
            "pos": Point(  # генерация случайной позиции для еды
                random.randint(0, (SCREEN_WIDTH//CELL_SIZE)-1),
                random.randint(0, (SCREEN_HEIGHT//CELL_SIZE)-1)
            ),
            "type": food_type,  # тип еды
            "spawn_time": time.get_ticks()  # время появления еды
        }
    
    # отрисовка еды
    def draw(self):
        food = self.current_food  # получаем текущую еду
        pygame.draw.rect(
            screen, 
            food["type"]["color"],
            (food["pos"].x*CELL_SIZE, food["pos"].y*CELL_SIZE, 
             CELL_SIZE, CELL_SIZE)  # отрисовываем еду
        )
        
        # для временной еды показываем оставшееся время
        if food["type"]["lifetime"]:
            remaining = (food["type"]["lifetime"] - (time.get_ticks() - food["spawn_time"])) // 1000
            if remaining > 0:  # если еда еще не истекла, показываем оставшееся время
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(remaining), True, BLACK)  # отображаем время в секундах
                screen.blit(text, 
                           (food["pos"].x*CELL_SIZE + 5, 
                            food["pos"].y*CELL_SIZE + 5))
    
    # проверка, не истекло ли время еды
    def check_expired(self):
        if self.current_food["type"]["lifetime"]:
            elapsed = time.get_ticks() - self.current_food["spawn_time"]  # проверяем время жизни еды
            return elapsed > self.current_food["type"]["lifetime"]  # если время вышло, возвращаем True
        return False

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
pygame.init()  # инициализация Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # создание экрана
pygame.display.set_caption("Змейка с уровнями и скоростью")  # название окна
clock = pygame.time.Clock()  # объект для контроля времени игры

# запрос имени пользователя
username = input("Введите ваше имя: ")  # запрашиваем имя пользователя
connecttobaza.execute('SELECT * FROM users WHERE username = %s', (username,))  # проверяем, есть ли пользователь в базе данных
user = connecttobaza.fetchone()  # извлекаем данные пользователя

if not user:  # если пользователя нет в базе данных
    connecttobaza.execute('INSERT INTO users (username) VALUES (%s) RETURNING id', (username,))  # регистрируем нового пользователя
    user_id = connecttobaza.fetchone()[0]  # получаем id нового пользователя
    connection.commit()  # применяем изменения в базе данных
    print(f"Пользователь {username} зарегистрирован!")  # выводим сообщение
else:  # если пользователь найден
    user_id = user[0]  # получаем id существующего пользователя
    print(f"Добро пожаловать обратно, {username}!")  # приветствуем пользователя

snake = Snake()  # создаем объект змейки
food = Food()  # создаем объект еды
game_active = True  # переменная для контроля активного состояния игры
paused = False  # переменная для паузы

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
while game_active:  # основной игровой цикл
    for event in pygame.event.get():  # обработка событий
        if event.type == pygame.QUIT:  # если нажали на крестик в окне
            game_active = False  # закрываем игру
        elif event.type == pygame.KEYDOWN:  # если нажата клавиша
            if event.key == pygame.K_UP:  # если нажата клавиша вверх
                snake.change_direction(0, -1)  # меняем направление на вверх
            elif event.key == pygame.K_DOWN:  # если нажата клавиша вниз
                snake.change_direction(0, 1)  # меняем направление на вниз
            elif event.key == pygame.K_LEFT:  # если нажата клавиша влево
                snake.change_direction(-1, 0)  # меняем направление на влево
            elif event.key == pygame.K_RIGHT:  # если нажата клавиша вправо
                snake.change_direction(1, 0)  # меняем направление на вправо
            elif event.key == pygame.K_p:  # если нажата клавиша для паузы
                paused = not paused  # меняем состояние паузы
                if paused:
                    print("Игра на паузе")  # выводим сообщение, если игра на паузе
                else:
                    print("Продолжение игры")  # выводим сообщение, если игра продолжается
    
    if not paused:  # если игра не на паузе
        snake.move()  # перемещаем змейку
        snake.increase_level()  # проверяем, не достигнут ли новый уровень

        # проверка съедания еды
        head = snake.body[0]  # берем голову змейки
        if (head.x == food.current_food["pos"].x and head.y == food.current_food["pos"].y):  # если змея съела еду
            snake.grow(food.current_food["type"]["weight"])  # увеличиваем змейку
            snake.score += food.current_food["type"]["weight"]  # увеличиваем очки
            food.current_food = food.generate_food()  # генерируем новую еду

        # проверка истечения времени еды
        if food.check_expired():  # если еда истекла по времени
            food.current_food = food.generate_food()  # генерируем новую еду

        # отрисовка
        screen.fill(BLACK)  # очищаем экран
        food.draw()  # отрисовываем еду
        snake.draw()  # отрисовываем змейку

        # отображение счета
        font = pygame.font.SysFont(None, 36)  # шрифт для текста
        score_text = font.render(f"Счет: {snake.score}", True, WHITE)  # текст с количеством очков
        screen.blit(score_text, (10, 10))  # отображаем счет на экране

        # отображение уровня
        level_text = font.render(f"Уровень: {snake.level}", True, WHITE)  # текст с уровнем
        screen.blit(level_text, (10, 40))  # отображаем уровень на экране

        pygame.display.flip()  # обновляем экран
        clock.tick(snake.speed)  # контролируем скорость игры

# сохранение очков в базу данных перед выходом
snake.save_score_to_db(user_id)  # сохраняем результат игры в базу данных

pygame.quit()  # завершаем работу Pygame
sys.exit()  # закрываем программу
