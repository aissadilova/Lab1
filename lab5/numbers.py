import re

def find_words_with_numbers(text):
    return re.findall(r'\b\w*\d\w*\b', text)

text = "I have 2 apples, 3bananas, and one orange123."
result = find_words_with_numbers(text)

print(result)


# 🔹 Разбор шаблона r'\b\w*\d\w*\b'
# \b   → Граница слова (ищем целые слова)
# \w*  → Любое количество букв или цифр перед числом (может быть пусто)
# \d   → Обязательно хотя бы одна цифра в слове
# \w*  → Любое количество букв или цифр после числа (может быть пусто)
# \b   → Граница слова (слово полностью)
