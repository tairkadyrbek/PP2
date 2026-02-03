#1 Exit the loop when i is 3
i = 1
while i < 6:
    print(i)
    if i == 3:
        break
    i += 1

#2 Stop after 3 tries
tries = 0
while True:
    print("Typing...")
    tries += 1
    if tries == 3:
        break
    
#3 Stop when password is correct
while True:
    password = input("Enter password: ")
    if password == "admin":
        print("access granted")
        break
    
#4 Stop when sum over 50
total = 0
i = 1
while True:
    total += i
    if total > 50:
        print("Total = ", total)
        break
    i += 1
    
#5 Stop after printing 5 stars
count = 0
while True:
    print("*")
    count += 1
    if count == 5:
        break