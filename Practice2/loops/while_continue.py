#1
i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)
    
#2
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)
    
#3
i = 0
while i < 10:
    i += 1
    if i > 5:
        continue
    print(i)
    
#4
words = ["hi", "", "python", "code"]
i = 0
while i < len(words):
    if words[i] == "":
        continue
    print(words[i])
    i += 1
    
#5
numbers = [-2, 4, -9, 12, 4]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        continue
    print(numbers[i])
    i += 1
    
