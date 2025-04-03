import pygame
import random
from pygame.locals import *

# Настройка игры
pygame.init()
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Мультяшные Гонки")

# Цвета (добавим BLACK)
SKY_BLUE = (135, 206, 235)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (255, 100, 100)
PLAYER_COLOR = (100, 100, 255)
COIN_COLOR = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  # Вот это я пропустил!

# Игрок
class Player:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 20
        self.speed = 5
    
    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, SKY_BLUE, (self.x + 15, self.y + 10, 20, 15))
        pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 10, 8, 5))
        pygame.draw.circle(screen, BLACK, (self.x + 15, self.y + self.height - 10), 8)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 15, self.y + self.height - 10), 8)
    
    def move(self, keys):
        if keys[K_LEFT] and self.x > 20:
            self.x -= self.speed
        if keys[K_RIGHT] and self.x < screen_width - self.width - 20:
            self.x += self.speed

# Остальной код остается без изменений...
# [Здесь должен быть весь остальной код из предыдущего примера]

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, ROAD_COLOR, (20, 0, screen_width-40, screen_height))
    
    # [Остальная часть игрового цикла...]
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()