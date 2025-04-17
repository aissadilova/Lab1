# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initialzing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SPEED = 4
COINS = 0
NEXT_SPEED_UP = 1

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("lab8/AnimatedStreet.png")
coin_img = pygame.image.load("lab8/Coin.png")

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


pygame.mixer.music.load("lab8/background.wav")
pygame.mixer.music.play(-1)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 2, 3])  # Вес монеты
        original_image = coin_img

        size = {
            1: (24, 24),
            2: (32, 32),
            3: (40, 40)
        }[self.value]

        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)

    def move(self):
        self.rect.move_ip(0, COIN_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Setting up Sprites
P1 = Player()
E1 = Enemy()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 2000)

# Game Loop
while True:

    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    coins_collected = pygame.sprite.spritecollide(P1, coins, True)
    for coin in coins_collected:
        COINS += coin.value
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 130, 10))

    if COINS >= NEXT_SPEED_UP:
        SPEED += 1
        NEXT_SPEED_UP += 1

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.Sound('lab8/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)