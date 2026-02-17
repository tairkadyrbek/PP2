#1 Arbitrary Arguments - *args
def my_function(*kids):
    print("The youngest child is " + kids[2])
    
my_function("Ryan", "Seth", "Jack")

#2 *args with Regular Arguments
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")

#3 Arbitrary Keyword Arguments - **kwargs
def calculate_total(**prices):
    total = 0
    for item in prices:
        total += prices[item]
    return total

result = calculate_total(apple=5, banana=6, orange=2)
print(result)   # 13

#4 Combining *args and **kwargs
def show(*args, **kwargs):
    print(args)
    print(kwargs)
    
show(1, 2, 3, name="Jack", age=18)

#5 Unpacking Arguments
def multiply(a, b, c):
    return a * b * c

values = {"a": 2, "b": 3, "c": 4}

result = multiply(**values)
print(result)   # 24


