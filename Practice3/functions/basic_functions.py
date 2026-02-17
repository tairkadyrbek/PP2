#1
def function():
    print("Hello, World!")

#2 Calling a function
def function():
    print("Hello")

function()

#3 Function with parameters
def function(fname):
    print("hello, ", fname)

function("Patrick")

#4 
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))

#5
def add(a, b):
    return a + b

print(add(8, 2))
