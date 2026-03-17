import shutil
import os

# Create a file to work with
file = open("original.txt", "w")
file.write("This is the original line\n")
file.write("It has some text inside\n")
file.close()

print("Original file created!")

# Copy the file
shutil.copy("original.txt", "copy.txt")
print("File copied to copy.txt")

# Make a backup
shutil.copy("original.txt", "original_backup.txt")
print("Backup created: original_backup.txt")

# Check if files exist
print("original.txt exists:", os.path.exists("original.txt"))
print("copy.txt exists:", os.path.exists("copy.txt"))
print("original_backup.txt exists:", os.path.exists("original_backup.txt"))

# Delete the copy file
os.remove("copy.txt")
print("copy.txt deleted!")

# Check again
print("copy.txt exists:", os.path.exists("copy.txt"))