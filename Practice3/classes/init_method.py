#1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
p1 = Person("Ryan", 17)

print(p1.name)
print(p1.age)

#2 Default Values in __init__()
class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Emil")
p2 = Person("Tobias", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)

#3 Multiple Parameters
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Ryan", 17, "Chino", "USA")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)

#4 Constructor storing a single value
class Student:
    def __init__(self, name):
        self.name = name

s = Student("Elliot")
print(s.name)

#5 Constructor with two attributes
class Phone:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

p = Phone("Samsung", 800)
print(p.brand, p.price)