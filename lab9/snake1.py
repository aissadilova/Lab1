import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 600  # Ширина экрана
HEIGHT = 600  # Высота экрана
CELL = 30  # Размер одной ячейки на поле
FPS = 5  # Начальная скорость игры

# Цвета для отрисовки
colorBLACK = (0, 0, 0)  # Черный цвет
colorRED = (255, 0, 0)  # Красный цвет (для головы змейки)
colorYELLOW = (255, 255, 0)  # Желтый цвет (для тела змейки)
colorGREEN = (0, 255, 0)  # Зеленый цвет (для еды)
colorGRAY = (169, 169, 169)  # Серый цвет (для сетки)
colorWHITE = (255, 255, 255)  # Белый цвет

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Экран с размерами WIDTH x HEIGHT

# Функция для отрисовки сетки
def draw_grid():
    # Создаем сетку, рисуя прямоугольники по всему экрану
    for i in range(HEIGHT // CELL):  # Проходим по вертикали
        for j in range(WIDTH // CELL):  # Проходим по горизонтали
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)  # Рисуем клетку

# Класс Point для хранения координат x и y
class Point:
    def __init__(self, x, y):
        self.x = x  # Координата x
        self.y = y  # Координата y

    def __str__(self):
        return f"{self.x}, {self.y}"  # Строковое представление точки

# Класс Snake для змейки
class Snake:
    def __init__(self):
        # Начальная позиция змейки (три сегмента)
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1  # Начальное направление по оси X (вправо)
        self.dy = 0  # Начальное направление по оси Y (вверх)

    def move(self):
        # Двигаем тело змейки, начиная с конца
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x  # Копируем координаты предыдущего сегмента по оси X
            self.body[i].y = self.body[i - 1].y  # Копируем координаты предыдущего сегмента по оси Y

        # Перемещаем голову змейки (в зависимости от направления)
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Проверка на столкновение с границей (стеной)
        if self.body[0].x > WIDTH // CELL - 1 or self.body[0].x < 0 or self.body[0].y > HEIGHT // CELL - 1 or self.body[0].y < 0:
            return True  # Если змейка вышла за пределы, возвращаем True для окончания игры
        return False  # Если все в порядке, возвращаем False

    def draw(self):
        # Отрисовываем голову змейки (красный цвет)
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        # Отрисовываем тело змейки (желтый цвет)
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        # Проверка, съела ли змейка еду
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:  # Если координаты головы змейки совпадают с едой
            self.body.append(Point(head.x, head.y))  # Добавляем новый сегмент в хвост
            food.generate_random_pos(self.body)  # Генерируем новую позицию для еды
            return True  # Возвращаем True, если еда съедена
        return False  # Возвращаем False, если еда не съедена

# Класс Food для еды
class Food:
    def __init__(self):
        self.pos = Point(9, 9)  # Начальная позиция еды

    def draw(self):
        # Отрисовываем еду (зеленый цвет)
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # Генерация случайной позиции для еды
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)  # Случайная координата x
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)  # Случайная координата y
            # Убедимся, что еда не будет генерироваться на теле змейки
            if all(segment.x != self.pos.x or segment.y != self.pos.y for segment in snake_body):
                break  # Если позиция не совпадает с телом змейки, выходим из цикла

# Основной игровой цикл
clock = pygame.time.Clock()  # Часы для контроля FPS
snake = Snake()  # Создаем объект змейки
food = Food()  # Создаем объект еды

running = True  # Флаг для продолжения игры
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если игрок закрыл окно, выходим из игры
            running = False
        if event.type == pygame.KEYDOWN:  # Если нажата клавиша, меняем направление змейки
            if event.key == pygame.K_RIGHT:  # Если нажата клавиша вправо
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:  # Если нажата клавиша влево
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:  # Если нажата клавиша вниз
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:  # Если нажата клавиша вверх
                snake.dx = 0
                snake.dy = -1

    # Заполнение экрана черным цветом
    screen.fill(colorBLACK)

    # Отрисовка сетки
    draw_grid()

    # Двигаем змейку и проверяем на столкновение
    if snake.move():  # Если змейка выходит за пределы, заканчиваем игру
        print("Game Over!")
        running = False

    # Проверяем, съела ли змейка еду
    snake.check_collision(food)

    # Отрисовываем змейку и еду
    snake.draw()
    food.draw()

    # Обновляем экран
    pygame.display.flip()

    # Управляем скоростью игры
    clock.tick(FPS)

# Завершаем работу Pygame
pygame.quit()
