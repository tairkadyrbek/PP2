#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)
    
#2
for x in "hello":
    print(x)
    
#3
for i in range(1, 10):
    print(i)
    
#4
s = 0
for i in range(1, 20):
    s += i
print("Sum is ", s)

#5
for i in range(1, 10):
    if i % 2 == 0:
        print(i)