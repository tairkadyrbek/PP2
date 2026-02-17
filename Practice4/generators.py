#1 Squares up to N
def squares_up_to(n):
    for i in range(n + 1):
        yield i * i


#2 Even numbers from 0 to n (comma separated)
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


#3 Numbers divisible by 3 and 4
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


#4 Generator squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


#5 Countdown from n to 0
def countdown(n):
    for i in range(n, -1, -1):
        yield i
        
        
#Examples
for num in squares_up_to(5):
    print(num)

print(",".join(str(x) for x in even_numbers(10)))

for num in divisible_by_3_and_4(50):
    print(num)

for num in squares(3, 6):
    print(num)

for num in countdown(5):
    print(num)