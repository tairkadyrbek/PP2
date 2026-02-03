#1
fruits = ["apple", "banana", "strawberry", "orange"]
for x in fruits:
  print(x)
  if x == "strawberry":
    break

#2
cars = ["Porsche", "Audi", "BMW"]
for x in cars:
  if x == "BMW":
    break
  print(x)

#3
for i in range(1, 10):
    if i == 7:
        break
    print(i)
    
#4
nums = [3, 5, -9, 10, 19]
for i in nums:
    if i < 0:
        break
    print(i)
    
#5
for ch in "Hello":
    if ch == "l":
        break
    print(ch)
