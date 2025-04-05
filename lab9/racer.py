import pygame
import sys
import random
import time
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Параметры игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
INITIAL_SPEED = 5
SPEED = INITIAL_SPEED
SCORE = 0
COINS_COLLECTED = 0
COINS_FOR_SPEED_BOOST = 5  # Количество монет для увеличения скорости

# Шрифты
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# Создание экрана
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")

class Enemy(pygame.sprite.Sprite):
    """Класс вражеской машины"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40)), 0

    def move(self):
        """Движение врага вниз по экрану"""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

class Player(pygame.sprite.Sprite):
    """Класс игрока"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """Управление игроком с клавиатуры"""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    """Класс монеты с разным весом (задание 1)"""
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])  # Случайный вес 1, 2 или 3
        
        # Разный внешний вид в зависимости от веса
        if self.weight == 1:
            self.image = pygame.Surface((20, 20))
            self.image.fill(YELLOW)
        elif self.weight == 2:
            self.image = pygame.Surface((25, 25))
            self.image.fill(GREEN)
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(PURPLE)
            
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        """Установка случайной начальной позиции"""
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 
                           random.randint(-100, -40))

    def move(self):
        """Движение монеты вниз"""
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

# Создание спрайтов
player = Player()
enemy = Enemy()
coin = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# Событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Основной игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2  # Постепенное увеличение скорости
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка
    DISPLAYSURF.fill(WHITE)
    
    # Отображение информации
    score_text = font.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    speed_text = font.render(f"Speed: {SPEED:.1f}", True, BLACK)
    
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coins_text, (10, 40))
    DISPLAYSURF.blit(speed_text, (10, 70))

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        DISPLAYSURF.fill(RED)
        game_over_text = big_font.render("GAME OVER", True, BLACK)
        final_score = font.render(f"Final Score: {SCORE}", True, BLACK)
        final_coins = font.render(f"Coins Collected: {COINS_COLLECTED}", True, BLACK)
        
        DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        DISPLAYSURF.blit(final_score, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 10))
        DISPLAYSURF.blit(final_coins, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40))
        
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Сбор монет (задание 1)
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    for coin in collected_coins:
        COINS_COLLECTED += coin.weight
        
        # Увеличение скорости при сборе N монет (задание 2)
        if COINS_COLLECTED % COINS_FOR_SPEED_BOOST == 0:
            SPEED += 1.0
            boost_text = font.render("SPEED BOOST!", True, RED)
            DISPLAYSURF.blit(boost_text, (SCREEN_WIDTH//2 - 70, 100))
            pygame.display.update()
            time.sleep(0.3)
        
        # Создание новой монеты
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    pygame.display.update()
    FramePerSec.tick(FPS) 