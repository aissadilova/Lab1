def trapezoid_area(height, base1, base2):
    return 0.5 * (base1 + base2) * height

# Input
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

# Calculation
area = trapezoid_area(height, base1, base2)

# Output
print(f"Expected Output: {area}")
5
