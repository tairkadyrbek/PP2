#1
students = [("Ryan", 17), ("Jack", 15), ("Zack", 18)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

#2 Sort strings by length
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

#3 Sort numbers in descending order
nums = [4, 1, 9, 2, 7]
sorted_nums = sorted(nums, key=lambda x: x, reverse=True)
print(sorted_nums)

#4 Sort words alphabetically
words = ["banana", "apple", "cherry"]
result = sorted(words, key=lambda x: x)
print(result)

#5 Sort words by last letter
words = ["apple", "banana", "cherry", "kiwi"]
sorted_words = sorted(words, key=lambda w: w[-1])
print(sorted_words)