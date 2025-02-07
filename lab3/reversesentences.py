def reverse_sentence():
    """Принимает строку и возвращает её с перевёрнутыми словами"""
    sentence = input("Введите предложение: ")  # Получаем строку от пользователя
    words = sentence.split()  # Разбиваем строку на список слов
    reversed_words = " ".join(reversed(words))  # Разворачиваем список слов и соединяем обратно
    return reversed_words  # Возвращаем результат

# Вызываем функцию и выводим результат
result = reverse_sentence()
print("Перевёрнутое предложение:", result)
