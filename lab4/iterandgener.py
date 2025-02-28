def square_generator(N):
    for i in range(N + 1):
        yield i ** 2


def even_numbers(n):
    return (str(i) for i in range(n + 1) if i % 2 == 0)


def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2


def countdown(n):
    for i in range(n, -1, -1):
        yield i


# Example usage
n = int(input("Enter a number for even numbers: "))
print(", ".join(even_numbers(n)))

print("\nNumbers divisible by 3 and 4:")
n = int(input("Enter a number for divisibility check: "))
for num in divisible_by_3_and_4(n):
    print(num, end=" ")

print("\n\nSquares in range:")
a, b = map(int, input("Enter range (a b): ").split())
for num in squares(a, b):
    print(num, end=" ")

print("\n\nCountdown:")
n = int(input("Enter a number for countdown: "))
for num in countdown(n):
    print(num, end=" ")
