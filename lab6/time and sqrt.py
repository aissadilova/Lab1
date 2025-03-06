import time
import math

nomer = int(input("Введите число: "))
vremiya = int(input("Введите задержку: "))

time.sleep(vremiya / 1000)
result = math.sqrt(nomer)

print(f"Root: {nomer} после {vremiya} milsec: {result}")
