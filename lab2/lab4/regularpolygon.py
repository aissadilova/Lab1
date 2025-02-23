import math

def regular_polygon_area(num_sides, side_length):
    return (num_sides * side_length ** 2) / (4 * math.tan(math.pi / num_sides))

# Input
num_sides = int(input("Input number of sides: "))
side_length = float(input("Input the length of a side: "))

# Calculation
area = regular_polygon_area(num_sides, side_length)

# Output
print(f"The area of the polygon is: {area:.2f}")
