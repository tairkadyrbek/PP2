# First create a file with some text
file = open("sample.txt", "w")
file.write("Hello my name is Tair\n")
file.write("I am learning Python\n")
file.write("This is line3\n")
file.close()

# Read the whole file at once
file = open("sample.txt", "r")
content = file.read()
file.close()

print(f"File content:\n{content}")


# Read line by line
file = open("sample.txt", "r")
lines = file.readlines()
file.close()

print("Reading line by line:")
for line in lines:
    print(line)
