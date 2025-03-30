import pygame
import os

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

# Функция для загрузки изображения кнопки
def load_button_image(image_path):
    """Функция для загрузки изображения кнопки."""
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        print(f"Ошибка: файл {image_path} не найден.")
        return None

# Загрузка кнопок (путь к кнопке "knopk.png" в папке lab7)
play_button_image = load_button_image("lab7/knopk.png")
next_button_image = load_button_image("lab7/knopk.png")

# Проверка наличия изображений
if not play_button_image or not next_button_image:
    print("Ошибка: Не удалось загрузить изображения кнопок.")
    pygame.quit()
    exit()

# Позиции кнопок
def get_button_position(center_x, center_y):
    """Функция для получения позиции кнопки на экране."""
    return pygame.Rect(center_x - 25, center_y - 25, 50, 50)  # Уменьшили размер кнопок до 50x50

# Середина экрана
center_x = 300
center_y = 200  # Середина экрана по вертикали

# Перемещаем кнопки чуть ниже середины и увеличиваем расстояние между ними
play_button_rect = get_button_position(center_x - 100, center_y + 30)  # Первая кнопка сдвинута влево на 100 пикселей
next_button_rect = get_button_position(center_x + 100, center_y + 30)  # Вторая кнопка сдвинута вправо на 100 пикселей

# Музыка и переключение треков
songs = ["lab7/guitar.mp3", "lab7/piano.mp3"]
current_song = 0  # Начальный индекс для первого трека

# Функция для воспроизведения музыки по индексу
def play_music(song_index):
    """Функция для воспроизведения музыки по индексу."""
    try:
        pygame.mixer.music.load(songs[song_index])
        pygame.mixer.music.play()
        print(f"Playing: {songs[song_index]}")
    except pygame.error as e:
        print(f"Ошибка при воспроизведении музыки: {e}")

# Изначальная загрузка первого трека
play_music(current_song)

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка кликов по кнопкам
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                # Воспроизведение первого трека при нажатии на первую кнопку
                play_music(0)

            elif next_button_rect.collidepoint(event.pos):
                # Воспроизведение второго трека при нажатии на вторую кнопку
                play_music(1)

    # Отображение кнопок на экране
    screen.fill((255, 255, 255))  # Очистка экрана
    screen.blit(play_button_image, play_button_rect)  # Отображение кнопки для первого трека
    screen.blit(next_button_image, next_button_rect)  # Отображение кнопки для второго трека
    
    pygame.display.flip()  # Обновление экрана

pygame.quit()
