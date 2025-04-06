import pygame
import sys
pygame.init()

width = 600
height = 600
red = (255, 0, 0)
white = (255, 255, 255)
speed = 2
radius = 25
screen = pygame.display.set_mode((width, height))
FPS = 60
Clock = pygame.time.Clock()
class Circle:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move (self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT]:
            self.x -= self.speed
        if keys [pygame.K_UP]:
            self.y -= self.speed
        if keys [pygame.K_DOWN]:
            self.y += self.speed
        if keys [pygame.K_RIGHT]:
            self.x += self.speed

    def draw (self, screen):
        pygame.draw.circle(screen, red, (self.x, self.y), self.radius)
circle = Circle(100, 100, 25, 5)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    circle.move()
   # screen.fill(white)
    circle.draw(screen)
    pygame.display.update()
    Clock.tick(FPS)
pygame.quit()
sys.exit()