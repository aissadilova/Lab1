import pygame
import random
from pygame.locals import *

# Настройка игры
pygame.init()
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Мультяшные Гонки")

# Цвета
SKY_BLUE = (135, 206, 235)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (255, 100, 100)
PLAYER_COLOR = (100, 100, 255)
COIN_COLOR = (255, 215, 0)
WHITE = (255, 255, 255)

# Игрок
class Player:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 20
        self.speed = 5
    
    def draw(self):
        # Рисуем мультяшную машинку
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))
        # Окошки
        pygame.draw.rect(screen, SKY_BLUE, (self.x + 15, self.y + 10, 20, 15))
        # Фары
        pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 10, 8, 5))
        # Колёса
        pygame.draw.circle(screen, BLACK, (self.x + 15, self.y + self.height - 10), 8)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 15, self.y + self.height - 10), 8)
    
    def move(self, keys):
        if keys[K_LEFT] and self.x > 20:
            self.x -= self.speed
        if keys[K_RIGHT] and self.x < screen_width - self.width - 20:
            self.x += self.speed

# Монетки
class Coin:
    def __init__(self):
        self.size = 25
        self.x = random.randint(30, screen_width - 30)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)
        self.value = random.choice([1, 1, 1, 2, 3])  # Чаще 1 очко
    
    def draw(self):
        # Рисуем блестящую монетку
        pygame.draw.circle(screen, COIN_COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(screen, (255, 255, 180), (self.x + 5, self.y - 5), 5)
    
    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.reset()
    
    def reset(self):
        self.x = random.randint(30, screen_width - 30)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)

# Враги
class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = random.randint(30, screen_width - 30)
        self.y = random.randint(-200, -100)
        self.speed = random.randint(4, 8)
    
    def draw(self):
        # Рисуем вражескую машинку
        pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, self.width, self.height))
        # Окошки
        pygame.draw.rect(screen, SKY_BLUE, (self.x + 15, self.y + 10, 20, 15))
        # Колёса
        pygame.draw.circle(screen, BLACK, (self.x + 15, self.y + self.height - 10), 8)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 15, self.y + self.height - 10), 8)
    
    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.reset()
            return 1  # +1 очко за пропущенную машинку
        return 0
    
    def reset(self):
        self.x = random.randint(30, screen_width - 30)
        self.y = random.randint(-200, -100)
        self.speed = random.randint(4, 8)

# Основные переменные
player = Player()
coins = [Coin() for _ in range(3)]
enemies = [Enemy()]
score = 0
coins_collected = 0
game_speed = 5
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Дорожная разметка
road_lines = []
for i in range(10):
    road_lines.append(pygame.Rect(screen_width//2 - 2, i*60, 4, 30))

# Главный цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # Управление
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    # Рисуем фон
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, ROAD_COLOR, (20, 0, screen_width-40, screen_height))
    
    # Дорожная разметка
    for line in road_lines:
        line.y += game_speed
        if line.y > screen_height:
            line.y = -30
        pygame.draw.rect(screen, WHITE, line)
    
    # Обновляем и рисуем монетки
    for coin in coins:
        coin.move()
        coin.draw()
        
        # Проверка сбора монетки
        if (player.x < coin.x + coin.size and
            player.x + player.width > coin.x and
            player.y < coin.y + coin.size and
            player.y + player.height > coin.y):
            coins_collected += coin.value
            coin.reset()
    
    # Обновляем и рисуем врагов
    for enemy in enemies:
        score += enemy.move()
        enemy.draw()
        
        # Проверка столкновения
        if (player.x < enemy.x + enemy.width and
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y):
            running = False
    
    # Рисуем игрока
    player.draw()
    
    # Отображаем счёт
    score_text = font.render(f"Очки: {score}", True, BLACK)
    coins_text = font.render(f"Монеты: {coins_collected}", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(coins_text, (20, 50))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()