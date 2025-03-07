import re

def find_words_with_numbers(text):
    return re.findall(r'\b\w*\d\w*\b', text)

text = "I have 2 apples, 3bananas, and one orange123."
result = find_words_with_numbers(text)

print(result)