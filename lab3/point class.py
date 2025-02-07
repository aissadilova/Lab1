import math

class Point:
    def __init__(self, x=0, y=0):
        """Создает точку с заданными координатами (по умолчанию (0, 0))"""
        self.x = x
        self.y = y
    
    def show(self):
        """Выводит координаты точки"""
        print(f"Координаты точки: ({self.x}, {self.y})")
    
    def move(self):
        """Позволяет пользователю изменить координаты точки"""
        self.x = int(input("Введите новую координату X: "))
        self.y = int(input("Введите новую координату Y: "))
    
    def dist(self, other):
        """Вычисляет расстояние между данной точкой и другой точкой"""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return round(distance, 2)

# Основной код работы программы
p1 = Point()
p1.move()
p1.show()

p2 = Point()
p2.move()
p2.show()

print("Расстояние между точками:", p1.dist(p2))
