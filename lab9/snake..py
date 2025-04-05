import pygame
import random
import sys
from pygame import time

# ==================== НАСТРОЙКИ ====================
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
FPS = 8

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# ==================== КЛАССЫ ====================
class Point:
    """Хранит координаты x и y"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    """Класс змейки с управлением и отрисовкой"""
    def __init__(self):
        self.body = [Point(5, 5), Point(4, 5), Point(3, 5)]
        self.dx, self.dy = 1, 0
        self.score = 0
        
    def move(self):
        """Движение змейки"""
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
        
    def draw(self):
        """Отрисовка змейки"""
        for segment in self.body[1:]:
            pygame.draw.rect(screen, YELLOW, 
                            (segment.x*CELL_SIZE, segment.y*CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, 
                        (self.body[0].x*CELL_SIZE, self.body[0].y*CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))
    
    def grow(self, amount=1):
        """Увеличение змейки"""
        for _ in range(amount):
            tail = self.body[-1]
            self.body.append(Point(tail.x, tail.y))
    
    def change_direction(self, new_dx, new_dy):
        """Изменение направления движения"""
        if (self.dx * new_dx == 0) and (self.dy * new_dy == 0):
            self.dx, self.dy = new_dx, new_dy

class Food:
    """Класс еды с разными типами"""
    def __init__(self):
        self.types = [
            {"color": GREEN, "weight": 1, "lifetime": None},  # Обычная еда
            {"color": BLUE, "weight": 2, "lifetime": 5000},    # Временная еда (5 сек)
            {"color": PURPLE, "weight": 3, "lifetime": 3000}   # Ценная еда (3 сек)
        ]
        self.current_food = self.generate_food()
        
    def generate_food(self):
        """Генерация случайной еды"""
        food_type = random.choices(
            self.types, 
            weights=[70, 20, 10],  # Вероятности появления
            k=1
        )[0]
        
        return {
            "pos": Point(
                random.randint(0, (SCREEN_WIDTH//CELL_SIZE)-1),
                random.randint(0, (SCREEN_HEIGHT//CELL_SIZE)-1)
            ),
            "type": food_type,
            "spawn_time": time.get_ticks()
        }
    
    def draw(self):
        """Отрисовка еды"""
        food = self.current_food
        pygame.draw.rect(
            screen, 
            food["type"]["color"],
            (food["pos"].x*CELL_SIZE, food["pos"].y*CELL_SIZE, 
             CELL_SIZE, CELL_SIZE)
        )
        
        # Для временной еды показываем оставшееся время
        if food["type"]["lifetime"]:
            remaining = (food["type"]["lifetime"] - (time.get_ticks() - food["spawn_time"])) // 1000
            if remaining > 0:
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(remaining), True, BLACK)
                screen.blit(text, 
                           (food["pos"].x*CELL_SIZE + 5, 
                            food["pos"].y*CELL_SIZE + 5))
    
    def check_expired(self):
        """Проверка, не истекло ли время еды"""
        if self.current_food["type"]["lifetime"]:
            elapsed = time.get_ticks() - self.current_food["spawn_time"]
            return elapsed > self.current_food["type"]["lifetime"]
        return False

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Улучшенная Змейка")
clock = pygame.time.Clock()

snake = Snake()
food = Food()
game_active = True

# ==================== ГЛАВНЫЙ ЦИКЛ ====================
while game_active:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)
    
    # Логика игры
    snake.move()
    
    # Проверка съедания еды
    head = snake.body[0]
    if (head.x == food.current_food["pos"].x and 
        head.y == food.current_food["pos"].y):
        snake.grow(food.current_food["type"]["weight"])
        snake.score += food.current_food["type"]["weight"]
        food.current_food = food.generate_food()
    
    # Проверка истечения времени еды
    if food.check_expired():
        food.current_food = food.generate_food()
    
    # Отрисовка
    screen.fill(BLACK)
    food.draw()
    snake.draw()
    
    # Отображение счета
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Счет: {snake.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()