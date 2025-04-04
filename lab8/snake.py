"""
ЗМЕЙКА НА PYGAME
Структурированная версия для легкого изучения
"""

# ==================== ИМПОРТЫ ====================
import pygame
import random
import sys

# ==================== НАСТРОЙКИ ====================
# Размеры окна
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20  # Размер одной клетки

# Скорость игры
FPS = 5

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # Голова змейки
GREEN = (0, 255, 0)    # Еда
YELLOW = (255, 255, 0) # Тело змейки

# ==================== КЛАССЫ ====================
class Point:
    """Класс для хранения координат"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    """Класс змейки"""
    def __init__(self):
        # Начальное положение змейки (3 сегмента)
        self.body = [
            Point(5, 5),  # Голова
            Point(4, 5),  # Первый сегмент тела
            Point(3, 5)   # Второй сегмент тела
        ]
        self.direction_x = 1  # Начальное направление: вправо
        self.direction_y = 0

    def move(self):
        """Двигаем змейку"""
        # Сначала двигаем все сегменты тела
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        
        # Затем двигаем голову
        self.body[0].x += self.direction_x
        self.body[0].y += self.direction_y

    def draw(self):
        """Отрисовываем змейку на экране"""
        # Сначала рисуем тело (чтобы голова была сверху)
        for segment in self.body[1:]:
            pygame.draw.rect(
                screen, 
                YELLOW,
                (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
        
        # Затем рисуем голову
        head = self.body[0]
        pygame.draw.rect(
            screen,
            RED,
            (head.x * CELL_SIZE, head.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    def grow(self):
        """Увеличиваем змейку при поедании еды"""
        tail = self.body[-1]  # Берем последний сегмент
        self.body.append(Point(tail.x, tail.y))  # Добавляем новый сегмент

    def change_direction(self, new_x, new_y):
        """Меняем направление движения"""
        # Защита от разворота на 180 градусов
        if (self.direction_x * new_x == 0) and (self.direction_y * new_y == 0):
            self.direction_x = new_x
            self.direction_y = new_y

class Food:
    """Класс еды"""
    def __init__(self):
        self.position = Point(9, 9)  # Начальное положение еды

    def draw(self):
        """Отрисовываем еду"""
        pygame.draw.rect(
            screen,
            GREEN,
            (self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    def respawn(self):
        """Перемещаем еду в случайное место"""
        self.position.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1)
        self.position.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1)

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Создаем объекты
snake = Snake()
food = Food()
game_active = True

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
while game_active:
    # ---------- Обработка событий ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        
        # Обработка нажатий клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)
    
    # ---------- Логика игры ----------
    # Проверка съедания еды
    if (snake.body[0].x == food.position.x and 
        snake.body[0].y == food.position.y):
        snake.grow()
        food.respawn()
    
    # Двигаем змейку
    snake.move()
    
    # ---------- Отрисовка ----------
    screen.fill(BLACK)  # Очищаем экран
    food.draw()         # Рисуем еду
    snake.draw()        # Рисуем змейку
    pygame.display.flip()  # Обновляем экран
    
    # Контроль FPS
    clock.tick(FPS)

# ==================== ВЫХОД ====================
pygame.quit()
sys.exit()