#1 Return Values
def get_greeting():
    return "Hello!"

message = get_greeting()
print(message)

#2
def multiply(a, b):
    return a * b

print(multiply(2, 3))

#3
def cube(x):
    return x ** 3

result = cube(5)
print(result)

#4
def rectangle(a, b):
    area = a * b
    perimeter = 2 * (a + b)
    return area, perimeter

a, p = rectangle(5, 4)
print(a)
print(p)

#5
def even_numbers(n):
    return [i for i in range(1, n + 1) if i % 2 == 0]

print(even_numbers(10)) # [2, 4, 6, 8, 10]
