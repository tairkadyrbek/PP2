#1 Using Lambda with filter()
nums = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, nums))
print(even_numbers)

#2 Filter negative numbers
nums = [3, 5, -2, 1, -9]
negatives = list(filter(lambda x: x < 0, nums))
print(negatives)

#3
words = ["hello", "welcome", "well", "programming"]
short_words = list(filter(lambda w: len(w) < 6, words))
print(short_words)

#4
nums = [2, 7, 13, 14, 24]
result = list(filter(lambda x: x % 7 == 0, nums))
print(result)

#5 Filter numbers greater than 10
nums = [5, 23, 9, 8, 15]
greater_than_ten = list(filter(lambda x: x > 10, nums))
print(greater_than_ten)