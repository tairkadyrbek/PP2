import os

# Create a simple folder
os.mkdir("my_folder")
print("Created: my_folder")

# Create nested folders
os.makedirs("my_folder/photos/2025")
print("Created: my_folder/photos/2025")

os.makedirs("my_folder/documents")
print("Created: my_folder/documents")

# Create some files inside the folders
file = open("my_folder/hello.txt", "w")
file.write("Hello World!")
file.close()

file = open("my_folder/documents/notes.txt", "w")
file.write("my notes")
file.close()

file = open("my_folder/documents/homework.py", "w")
file.write("# homework file")
file.close()

# List files and folders inside my_folder
print("\nFiles and folders in my_folder:")
items = os.listdir("my_folder")
for item in items:
    print(" -", item)

# List files inside documents folder
print("\nFiles in my_folder/documents:")
items = os.listdir("my_folder/documents")
for item in items:
    print(" -", item)
    
# Find files by extension (.txt)
print("\nAll .txt files in my_folder")
for root, dirs, files in os.walk("my_folder"):
    for file in files:
        if file.endswith(".txt"):
            print(" -", os.path.join(root, file))
            
# Find files by extenstion (.py)
print("\nAll .py files in my_folder:")
for root, dirs, files in os.walk("my_folder"):
    for file in files:
        if file.endswith(".py"):
            print(" -", os.path.join(root, file))
