class Shape:
    def area(self):
        """Возвращает площадь фигуры (по умолчанию 0)"""
        return 0

class Rectangle(Shape):
    def __init__(self):
        """Создает пустой прямоугольник, параметры вводятся пользователем"""
        self.length = 0
        self.width = 0
    
    def get_dimensions(self):
        """Запрашивает у пользователя длину и ширину прямоугольника"""
        self.length = int(input("Введите длину прямоугольника: "))
        self.width = int(input("Введите ширину прямоугольника: "))
    
    def area(self):
        """Вычисляет площадь прямоугольника"""
        return self.length * self.width

# Основной код работы программы
rect = Rectangle()
rect.get_dimensions()
print("Площадь прямоугольника:", rect.area())
