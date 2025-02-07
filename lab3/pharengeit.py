def fahrenheit_to_celsius(f):
    """Преобразует температуру из Фаренгейта в Цельсий"""
    return (5 / 9) * (f - 32)

fahrenheit = float(input("Введите температуру в Фаренгейтах: "))
celsius = fahrenheit_to_celsius(fahrenheit)
print(f"Температура в градусах Цельсия: {celsius:.2f}")