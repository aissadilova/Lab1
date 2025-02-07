import math

def is_prime(n):
    """Проверяет, является ли число простым"""
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

# Используем filter и lambda для фильтрации простых чисел
numbers = list(map(int, input("Введите список чисел через пробел: ").split()))
prime_numbers = list(filter(lambda x: is_prime(x), numbers))

print("Простые числа в списке:", prime_numbers)
