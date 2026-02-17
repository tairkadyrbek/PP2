#1 Using Lambda with map()
numbers = [1, 3 , 5, 7, 9]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

#2
numbers = [2, 3, 4]
square = list(map(lambda x: x ** 2, numbers))
print(square)

#3 Subtract 2 from each number
nums = [10, 20, 30]
result = list(map(lambda x: x - 2, nums))
print(result)

#4 Get first letter of each word
words = ["Apple", "Banana", "Cherry"]
first_letter = list(map(lambda w: w[0], words))
print(first_letter)

#5 Convert numbers to absolute values
nums = [-5, -7, 2, -12]
absolute = list(map(lambda x: abs(x), nums))
print(absolute)