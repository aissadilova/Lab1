import pygame
import random

# Инициализация PyGame
pygame.init()

# Настройки экрана
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racer: Collect Coins")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Шрифты
font = pygame.font.SysFont("comicsansms", 72)
font_small = pygame.font.SysFont("comicsansms", 30)

# Игрок (машина)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80), pygame.SRCALPHA)  # Прозрачный фон
        pygame.draw.rect(self.image, BLUE, (0, 0, 50, 80))      # Синий прямоугольник
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 100)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)  # Жёлтый круг
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = random.randint(3, 7)

    def reset_position(self):
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.reset_position()

# Создание объектов
player = Player()
all_sprites = pygame.sprite.Group(player)
coins = pygame.sprite.Group()

# Генерация 10 монет
for _ in range(10):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Счётчик
score = 0
clock = pygame.time.Clock()
running = True

# Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Проверка столкновений
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        score += 1
        new_coin = Coin()
        all_sprites.add(new_coin)
        coins.add(new_coin)

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Счётчик
    score_text = font_small.render(f"Coins: {score}", True, WHITE)
    screen.blit(score_text, (screen_width - 150, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()