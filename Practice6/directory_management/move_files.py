import shutil
import os

# Create two folders
os.makedirs("folder_a", exist_ok=True)
os.makedirs("folder_b", exist_ok=True)

# Create some files in folder_a
file = open("folder_a/file1.txt", "w")
file.write("This is file 1")
file.close()

file = open("folder_a/file2.txt", "w")
file.write("This is file 2")
file.close()

file = open("folder_a/file3.txt", "w")
file.write("This is file 3")
file.close()

print("Files in folder_a:", os.listdir("folder_a"))
print("Files in folder_b", os.listdir("folder_b"))

# Copy a file from folder_a to folder_b
shutil.copy("folder_a/file1.txt", "folder_b/file1.txt")
print("\nCopied file1.txt to folder_b")

# Move a file from folder_a to folder_b
shutil.move("folder_a/file2.txt", "folder_b/file2.txt")
print("Moved file2.txt to folder_b")

# Check folders after copy and move
print("\nAfter copy and move:")
print("Files in folder_a", os.listdir("folder_a"))
print("Files in folder_b", os.listdir("folder_b"))

