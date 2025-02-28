def parallelogram_area(base, height):
    return base * height

# Input
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

# Calculation
area = parallelogram_area(base, height)

# Output
print(f"Expected Output: {area:.1f}")
