#1
x = lambda a : a + 20
print(x(7))

#2
x = lambda a, b : a * b
print(x(2,7))

#3
def myfunc(n):
    return lambda a : a * n

mydoubler = myfunc(2)
print(mydoubler(19))

#4
x = lambda a : a ** 2
print(x(7))

#5
x = lambda a, b : a / b
print(x(36, 6))
