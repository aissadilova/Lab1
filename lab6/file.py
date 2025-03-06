import os

path = input("Введите файл: ")

items = []

if os.path.exists(path):
    items = os.listdir(path)

print("Папки: ")

for item in items:
    if os.path.isdir(os.path.join(path, item)):
                     print(item)

print ("Файлы: ")

for item in items: 
       if os.path.isfile(os.path.join(path, item)):
            print(item)

print("Все: ")
for item in items:
    print(item)


else:
  print("Папка не найденаа")