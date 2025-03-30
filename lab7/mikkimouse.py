import pygame
import time

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# Загрузка изображений
face = pygame.image.load('clock.png')
minute_hand = pygame.image.load('min_hand.png')
second_hand = pygame.image.load('sec_hand.png')

# Масштабирование при необходимости
face = pygame.transform.scale(face, (WIDTH, HEIGHT))

# Получение размеров стрелок
mw, mh = minute_hand.get_size()
sw, sh = second_hand.get_size()

# Центр часов
center = (WIDTH // 2, HEIGHT // 2)

def blitRotate(surf, image, pos, pivot, angle):
    """Функция для вращения изображения вокруг заданной точки"""
    rotated_image = pygame.transform.rotate(image, -angle)  # Отрицательный угол для движения по часовой стрелке
    new_rect = rotated_image.get_rect(center=(pos[0], pos[1]))
    surf.blit(rotated_image, new_rect)

# Основной цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))
    screen.blit(face, (0, 0))

    # Получаем текущее время
    current_time = time.localtime()
    seconds = current_time.tm_sec - 10
    minutes = current_time.tm_min + 9

    print(f"Minute: {minutes}, Second: {seconds}")

    # Вычисляем углы
    sec_angle = seconds * 6  # 360° / 60 = 6° за 1 секунду
    min_angle = (minutes + seconds / 60) * 6  # Учитываем прошедшие секунды

    # Рисуем стрелки (центр вращения теперь корректен)
    blitRotate(screen, second_hand, center, (sw // 2, sh - 20), sec_angle)
    blitRotate(screen, minute_hand, center, (mw // 2, mh - 20), min_angle)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(1)  # Ограничение FPS

pygame.quit()