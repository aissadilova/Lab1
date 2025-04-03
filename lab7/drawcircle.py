import pygame

pygame.init()

screen_width = 800
screen_height = 600
ball_radius = 25
ball_speed = 20
ball_x = screen_width // 2
ball_y = screen_height // 2

white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Game")

running = True
while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if ball_y - ball_radius > 0:
            ball_y -= ball_speed
    if keys[pygame.K_DOWN]:
        if ball_y + ball_radius < screen_height:
            ball_y += ball_speed
    if keys[pygame.K_LEFT]:
        if ball_x - ball_radius > 0:
            ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        if ball_x + ball_radius < screen_width:
            ball_x += ball_speed

    pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)

    pygame.display.update()

pygame.quit()
