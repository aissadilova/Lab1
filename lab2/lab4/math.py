import math

def degree_to_radian(degree):
    return degree * (math.pi / 180)

# Input
degree = float(input("Input degree: "))

# Conversion
radian = degree_to_radian(degree)

# Output
print(f"Output radian: {radian:.6f}")
