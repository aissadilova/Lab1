import os

path = input("Введи крч: ")

print("проверка пути:", path)
print("Exist:", os.access(path, os.F_OK))
print("Readable:", os.access(path, os.R_OK))
print("Writeaable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))
