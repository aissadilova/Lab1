import pygame
import random
import sys
import psycopg2
from pygame import time

# Подключаемся к базе данных
connection = psycopg2.connect(dbname="snakegame", user="postgres", password="postgres", host="localhost")  # Устанавливаем соединение с PostgreSQL
connecttobaza = connection.cursor()  # Создаем объект для выполнения SQL-запросов

# Создание таблицы пользователей, если она не существует
connecttobaza.execute(
    'CREATE TABLE IF NOT EXISTS users('  # Запрос на создание таблицы пользователей
    'id SERIAL PRIMARY KEY, '  # Поле id будет уникальным идентификатором
    'username TEXT UNIQUE'  # Имя пользователя должно быть уникальным
    ')'
)
connection.commit()  # Применяем изменения в базе данных

# Создание таблицы для хранения очков пользователей, если она не существует
connecttobaza.execute(
    'CREATE TABLE IF NOT EXISTS user_score('  # Запрос на создание таблицы очков
    'id SERIAL PRIMARY KEY, '  # Поле id для уникальности
    'user_id INTEGER, '  # Поле для хранения id пользователя
    'level INTEGER, '  # Поле для хранения уровня игрока
    'score INTEGER, '  # Поле для хранения очков игрока
    'FOREIGN KEY(user_id) REFERENCES users(id) '  # Связь с таблицей users через user_id
    ')'
)
connection.commit()  # Применяем изменения в базе данных

# ==================== Настройки ====================
SCREEN_WIDTH = 600  # Ширина экрана игры
SCREEN_HEIGHT = 400  # Высота экрана игры
CELL_SIZE = 20  # Размер ячеек, в которых будет двигаться змейка
FPS = 8  # Начальная скорость игры

# Цвета
BLACK = (0, 0, 0)  # Черный цвет для фона
RED = (255, 0, 0)  # Красный для головы змейки
GREEN = (0, 255, 0)  # Зеленый для обычной еды
YELLOW = (255, 255, 0)  # Желтый для тела змейки
BLUE = (0, 0, 255)  # Синий для специальной еды
PURPLE = (128, 0, 128)  # Фиолетовый для ценной еды
WHITE = (255, 255, 255)  # Белый цвет для текста

# ==================== Классы ====================
class Point:
    """Класс для хранения координат x и y"""
    def __init__(self, x, y):
        self.x = x  # Координата x
        self.y = y  # Координата y

class Snake:
    """Класс змейки с логикой управления и отрисовки"""
    def __init__(self):
        self.body = [Point(5, 5), Point(4, 5), Point(3, 5)]  # Начальная позиция змейки
        self.dx, self.dy = 1, 0  # Направление змейки (вправо)
        self.score = 0  # Начальные очки
        self.speed = 5  # Начальная скорость змейки
        self.level = 1  # Начальный уровень
        self.walls = []  # Список стен, которые будут добавлены в уровне

    def move(self):
        """Функция для перемещения змейки"""
        for i in range(len(self.body)-1, 0, -1):  # Сдвигаем каждый сегмент тела змейки
            self.body[i].x = self.body[i-1].x  # Перемещаем сегменты
            self.body[i].y = self.body[i-1].y  # Перемещаем сегменты
        self.body[0].x += self.dx  # Перемещаем голову змейки по оси x
        self.body[0].y += self.dy  # Перемещаем голову змейки по оси y

    def draw(self):
        """Функция для отрисовки змейки"""
        for segment in self.body[1:]:  # Отрисовываем тело змейки
            pygame.draw.rect(screen, YELLOW, 
                            (segment.x*CELL_SIZE, segment.y*CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, 
                        (self.body[0].x*CELL_SIZE, self.body[0].y*CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))  # Отрисовываем голову змейки
    
    def grow(self, amount=1):
        """Функция для увеличения змейки"""
        for _ in range(amount):  # Добавляем новые сегменты тела змейки
            tail = self.body[-1]  # Берем последний сегмент змейки
            self.body.append(Point(tail.x, tail.y))  # Добавляем новый сегмент
    
    def change_direction(self, new_dx, new_dy):
        """Изменение направления движения"""
        if (self.dx * new_dx == 0) and (self.dy * new_dy == 0):  # Проверка, чтобы нельзя было двигаться в противоположную сторону
            self.dx, self.dy = new_dx, new_dy  # Обновляем направление змейки

    def increase_level(self):
        """Увеличение уровня"""
        if self.score >= self.level * 2:  # Уровень увеличивается каждые 10 очков
            self.level += 1  # Увеличиваем уровень
            self.speed += 1  # Увеличиваем скорость на каждом уровне
            self.create_walls()  # Создаем новые стены для следующего уровня

    def create_walls(self):
        """Генерация стен для нового уровня"""
        self.walls = []  # Очищаем старые стены
        if self.level == 2:
            self.walls = [Point(10, 5), Point(11, 5), Point(12, 5)]  # Пример стены для уровня 2
        elif self.level == 3:
            self.walls = [Point(8, 3), Point(9, 3), Point(10, 3), Point(11, 3)]  # Пример стены для уровня 3

    def save_score_to_db(self, user_id):
        """Сохранение текущего счета в базу данных"""
        connecttobaza.execute(
            'INSERT INTO user_score (user_id, level, score) '
            'VALUES (%s, %s, %s)', (user_id, self.level, self.score)  # Записываем очки и уровень в базу
        )
        connection.commit()  # Применяем изменения в базе данных

class Food:
    """Класс еды с разными типами"""
    def __init__(self):
        self.types = [
            {"color": GREEN, "weight": 1, "lifetime": None},  # Обычная еда
            {"color": BLUE, "weight": 2, "lifetime": 5000},   # Временная еда (5 сек)
            {"color": PURPLE, "weight": 3, "lifetime": 3000}  # Ценная еда (3 сек)
        ]
        self.current_food = self.generate_food()  # Генерируем начальную еду
        
    def generate_food(self):
        """Генерация случайной еды"""
        food_type = random.choices(
            self.types, 
            weights=[70, 20, 10],  # Вероятности появления разных типов еды
            k=1
        )[0]
        
        return {
            "pos": Point(  # Генерация случайной позиции для еды
                random.randint(0, (SCREEN_WIDTH//CELL_SIZE)-1),
                random.randint(0, (SCREEN_HEIGHT//CELL_SIZE)-1)
            ),
            "type": food_type,  # Тип еды
            "spawn_time": time.get_ticks()  # Время появления еды
        }
    
    def draw(self):
        """Отрисовка еды"""
        food = self.current_food  # Получаем текущую еду
        pygame.draw.rect(
            screen, 
            food["type"]["color"],
            (food["pos"].x*CELL_SIZE, food["pos"].y*CELL_SIZE, 
             CELL_SIZE, CELL_SIZE)  # Отрисовываем еду
        )
        
        # Для временной еды показываем оставшееся время
        if food["type"]["lifetime"]:
            remaining = (food["type"]["lifetime"] - (time.get_ticks() - food["spawn_time"])) // 1000
            if remaining > 0:  # Если еда еще не истекла, показываем оставшееся время
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(remaining), True, BLACK)  # Отображаем время в секундах
                screen.blit(text, 
                           (food["pos"].x*CELL_SIZE + 5, 
                            food["pos"].y*CELL_SIZE + 5))
    
    def check_expired(self):
        """Проверка, не истекло ли время еды"""
        if self.current_food["type"]["lifetime"]:
            elapsed = time.get_ticks() - self.current_food["spawn_time"]  # Проверяем время жизни еды
            return elapsed > self.current_food["type"]["lifetime"]  # Если время вышло, возвращаем True
        return False

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создание экрана
pygame.display.set_caption("Змейка с уровнями и скоростью")  # Название окна
clock = pygame.time.Clock()  # Объект для контроля времени игры

# Запрос имени пользователя
username = input("Введите ваше имя: ")  # Запрашиваем имя пользователя
connecttobaza.execute('SELECT * FROM users WHERE username = %s', (username,))  # Проверяем, есть ли пользователь в базе данных
user = connecttobaza.fetchone()  # Извлекаем данные пользователя

if not user:  # Если пользователя нет в базе данных
    connecttobaza.execute('INSERT INTO users (username) VALUES (%s) RETURNING id', (username,))  # Регистрируем нового пользователя
    user_id = connecttobaza.fetchone()[0]  # Получаем id нового пользователя
    connection.commit()  # Применяем изменения в базе данных
    print(f"Пользователь {username} зарегистрирован!")  # Выводим сообщение
else:  # Если пользователь найден
    user_id = user[0]  # Получаем id существующего пользователя
    print(f"Добро пожаловать обратно, {username}!")  # Приветствуем пользователя

snake = Snake()  # Создаем объект змейки
food = Food()  # Создаем объект еды
game_active = True  # Переменная для контроля активного состояния игры
paused = False  # Переменная для паузы

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
while game_active:  # Основной игровой цикл
    for event in pygame.event.get():  # Обработка событий
        if event.type == pygame.QUIT:  # Если нажали на крестик в окне
            game_active = False  # Закрываем игру
        elif event.type == pygame.KEYDOWN:  # Если нажата клавиша
            if event.key == pygame.K_UP:  # Если нажата клавиша вверх
                snake.change_direction(0, -1)  # Меняем направление на вверх
            elif event.key == pygame.K_DOWN:  # Если нажата клавиша вниз
                snake.change_direction(0, 1)  # Меняем направление на вниз
            elif event.key == pygame.K_LEFT:  # Если нажата клавиша влево
                snake.change_direction(-1, 0)  # Меняем направление на влево
            elif event.key == pygame.K_RIGHT:  # Если нажата клавиша вправо
                snake.change_direction(1, 0)  # Меняем направление на вправо
            elif event.key == pygame.K_p:  # Если нажата клавиша для паузы
                paused = not paused  # Меняем состояние паузы
                if paused:
                    print("Игра на паузе")  # Выводим сообщение, если игра на паузе
                else:
                    print("Продолжение игры")  # Выводим сообщение, если игра продолжается
    
    if not paused:  # Если игра не на паузе
        snake.move()  # Перемещаем змейку
        snake.increase_level()  # Проверяем, не достигнут ли новый уровень

        # Проверка съедания еды
        head = snake.body[0]  # Берем голову змейки
        if (head.x == food.current_food["pos"].x and head.y == food.current_food["pos"].y):  # Если змея съела еду
            snake.grow(food.current_food["type"]["weight"])  # Увеличиваем змейку
            snake.score += food.current_food["type"]["weight"]  # Увеличиваем очки
            food.current_food = food.generate_food()  # Генерируем новую еду

        # Проверка истечения времени еды
        if food.check_expired():  # Если еда истекла по времени
            food.current_food = food.generate_food()  # Генерируем новую еду

        # Отрисовка
        screen.fill(BLACK)  # Очищаем экран
        food.draw()  # Отрисовываем еду
        snake.draw()  # Отрисовываем змейку

        # Отображение счета
        font = pygame.font.SysFont(None, 36)  # Шрифт для текста
        score_text = font.render(f"Счет: {snake.score}", True, WHITE)  # Текст с количеством очков
        screen.blit(score_text, (10, 10))  # Отображаем счет на экране

        # Отображение уровня
        level_text = font.render(f"Уровень: {snake.level}", True, WHITE)  # Текст с уровнем
        screen.blit(level_text, (10, 40))  # Отображаем уровень на экране

        pygame.display.flip()  # Обновляем экран
        clock.tick(snake.speed)  # Контролируем скорость игры

# Сохранение очков в базу данных перед выходом
snake.save_score_to_db(user_id)  # Сохраняем результат игры в базу данных

pygame.quit()  # Завершаем работу Pygame
sys.exit()  # Закрываем программу
