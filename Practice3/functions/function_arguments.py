#1 
def function(fname):    # fname is a parameter
    print(fname + " Cohen")
    
function("Seth")    # "Seth" is an argument
function("Sandy")

#2 Number of Arguments
def my_function(fname, lname):
    print(fname + " " + lname)
    
my_function("Ryan", "Atwood")

#3 Default Parameter Values
def my_function(name = "Jack"):
    print("Hello", name)
    
my_function("Emil")
my_function()   # the function is called without an argument

#4 Keyword Arguments
def my_function(animal, name):
    print("I have a", animal)
    print("My", animal + "'s name is", name)
    
my_function(animal = "cat", name = "Simba")

#5 Passing Different Data Types
def my_function(fruits):
    for fruit in fruits:
        print(fruit)
        
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)
