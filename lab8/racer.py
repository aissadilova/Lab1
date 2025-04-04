import pygame
pygame.init()

# Делаем окошко
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Моя рисовалка")

# Цвета
белый = (255, 255, 255)
красный = (255, 0, 0)

# Переменные для рисования
рисую = False
толщина = 3
начало_x, начало_y = 0, 0
конец_x, конец_y = 0, 0

# Очищаем экран
screen.fill(белый)
pygame.display.flip()

# Главный цикл
работает = True
while работает:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            работает = False
        
        # Нажали мышку
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            рисую = True
            начало_x, начало_y = event.pos
            конец_x, конец_y = event.pos
        
        # Двигаем мышку
        if event.type == pygame.MOUSEMOTION:
            if рисую:
                конец_x, конец_y = event.pos
                screen.fill(белый)  # Очищаем
                # Рисуем прямоугольник
                rect = pygame.Rect(
                    min(начало_x, конец_x),
                    min(начало_y, конец_y),
                    abs(конец_x - начало_x),
                    abs(конец_y - начало_y)
                )
                pygame.draw.rect(screen, красный, rect, толщина)
        
        # Отпустили мышку
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            рисую = False
        
        # Меняем толщину
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:  # Плюс
                толщина += 1
            elif event.key == pygame.K_MINUS:  # Минус
                if толщина > 1:
                    толщина -= 1
    
    pygame.display.flip()

pygame.quit()