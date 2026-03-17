# Create a new file and write some data
file = open("notes.txt", "w")
file.write("This is my first line\n")
file.write("This is my second line\n")
file.write("This is my third line\n")
file.close()

print("File created and written!")

# Append new lines to the same file
file = open("notes.txt", "a")
file.write("This line was appended\n")
file.write("Hello World!\n")
file.close()

print("New lines appended!")

file = open("notes.txt", "r")
content = file.read()
file.close()

print(f"Final file content:\n{content}")
