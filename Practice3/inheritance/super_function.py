#1 Simple inheritance with super
class Parent:
    def __init__(self):
        print("Parent constructor")

class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child constructor")

c = Child()

#2 Call parent constructor
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name)

s = Student("Ryan")
print(s.name)

#3 Add new attribute
class Animal:
    def __init__(self, type):
        self.type = type

class Dog(Animal):
    def __init__(self, type, name):
        super().__init__(type)
        self.name = name

d = Dog("Mammal", "Rex")
print(d.type, d.name)

#4 Call parent method
class A:
    def hello(self):
        print("Hello from A")

class B(A):
    def hello(self):
        super().hello()
        print("Hello from B")

b = B()
b.hello()

#5 Extend parent behavior
class Vehicle:
    def start(self):
        print("Vehicle starts")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car ready")

c = Car()
c.start()