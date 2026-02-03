#1
a = 3
b = 1
if a > b: print("a is greater than b")

#2
a = 19
b = 239
print("A") if a > b else print("B")

#3
a = 10
b = 19
bigger = a if a > b else b
print("Bigger is ", bigger)

#4
a = 250
b = 250
print("A") if a > b else print("=") if a == b else print("B")

#5
x = 39
y = 10
max_value = x if x > y else y
print("Maximum value:", max_value)

#6
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
