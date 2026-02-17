#1 Basic inheritance
class Shape:
    def draw(self):
        print("Shape drawn")

class Circle(Shape):
    pass

c = Circle()
c.draw()

#2
class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def honk(self):
        print("Car honks")

car = Car()
car.move()
car.honk()

#3 Inherit class variable
class Person:
    species = "Human"

class Student(Person):
    pass

s = Student()
print(s.species)

#4 Simple method inheritance
class Teacher:
    def teach(self):
        print("Teaching")

class MathTeacher(Teacher):
    pass

m = MathTeacher()
m.teach()

#5 Inherit and use parent method
class User:
    def login(self):
        print("User logged in")

class Admin(User):
    pass

a = Admin()
a.login()