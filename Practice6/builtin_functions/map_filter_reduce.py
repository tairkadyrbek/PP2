from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() - do something to every item in a list
# here we double every number
doubled = list(map(lambda x: x * 2, numbers))
print("Original numbers:", numbers)
print("Doubled with map:", doubled)

# filter() - keep only items that pass a condition
# here we keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers with filter:", evens)

# keep only odd numbers
odds = list(filter(lambda x: x % 2 != 0, numbers))
print("Even numbers with filter:", odds)

# reduce() - combine all items into one value
# here we add all numbers together
total = reduce(lambda x, y: x + y, numbers)
print("Sum with reduce:", total)

# Type checking
print("\n--- Type checking ---")
name = "Alima"
age = 20
gpa = 3.8
 
print("name is str:", isinstance(name, str))
print("age is int:", isinstance(age, int))
print("gpa is float:", isinstance(gpa, float))
 
# Type conversion
print("\n--- Type conversion ---")
number_as_string = "42"
print("Before:", number_as_string, type(number_as_string))
 
number_as_int = int(number_as_string)
print("After int():", number_as_int, type(number_as_int))
 
number_as_float = float(number_as_string)
print("After float():", number_as_float, type(number_as_float))
 
back_to_string = str(number_as_int)
print("After str():", back_to_string, type(back_to_string))