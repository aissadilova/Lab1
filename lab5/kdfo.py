import re

def find_upper_followed_by_lower(text):
    return re.findall(r'[A-Z][a-z]*', text)

text = "I am drinking Starbucks Lol"
result = find_upper_followed_by_lower(text)

print(result)