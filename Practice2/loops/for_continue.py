#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
  
#2
for i in range(1, 10):
    if i % 2 == 0:
        continue
    print(i)
    
#3
nums = [2, 52, 32, -23]
for i in nums:
    if i < 0:
        continue
    print(i)
    
#4
for ch in "Hello":
    if ch == "l":
        continue
    print(ch)
    
#5
password = "pa$$w0rd242"

for ch in password:
    if ch.isdigit():
        continue
    print(ch)
    