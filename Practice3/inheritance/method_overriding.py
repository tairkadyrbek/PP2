#1 Simple override
class Parent:
    def show(self):
        print("Parent method")

class Child(Parent):
    def show(self):
        print("Child method")

Child().show()

#2 Override with different message
class Animal:
    def sound(self):
        print("Some sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

Dog().sound()

#3 Override return value
class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def area(self):
        return 10

print(Rectangle().area())

#4 Override and use super()
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        super().greet()
        print("I am a student")

Student().greet()

#5 Override with condition
class Account:
    def withdraw(self, amount):
        print(f"Withdrew {amount}")

class PremiumAccount(Account):
    def withdraw(self, amount):
        if amount > 500:
            print("Too much!")
        else:
            super().withdraw(amount)

PremiumAccount().withdraw(300)
PremiumAccount().withdraw(700)