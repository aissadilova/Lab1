slovo = input("napishi slovo: ")

upper_count = sum(1 for char in slovo if char.isupper())

lower_count = sum(1 for char in slovo if char.islower())

print("Up: ", upper_count)
print("Low:", lower_count)