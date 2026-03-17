# enumerate() - gives you index and value at the same time
fruits = ["apple", "banana", "cherry", "mango"]

print("Using enumerate:")
for i, fruit in enumerate(fruits):
    print(i, fruit)

# You can also start counting from 1
print("\nUsing enumerate starting from 1:")
for i, fruit in enumerate(fruits, 1):
    print(i, fruit)
    
# zip() - combine two lists together
names = ["Amir", "Dana", "Saya"]
scores = [85, 92, 78]

print("\nUsing zip:")
for name, score in zip(names, scores):
    print(name, "got", score)

# zip() wuth three lists
players = ["Messi", "Ronaldo", "Neymar"]
goals = [45, 38, 29]
teams = ["Inter Miami", "Al Nassr", "Al Hilal"]

for player, goal, team in zip(players, goals, teams):
    print(player, "scored", goal, "goals for", team)
    
# zip() to make a dictionary
print("\nMaking a dictionary with zip:")
student_scores = dict(zip(names, scores))
print(student_scores)