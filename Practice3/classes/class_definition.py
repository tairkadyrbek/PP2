#1
class MyClass:
    x = 5
    
obj = MyClass()
print(obj.x)

#2 Class with two attributes
class Laptop:
    brand = "HP"
    ram = 16

l = Laptop()
print(l.brand, l.ram)

#3 Empty class example
class Test:
    pass

t = Test()
print(type(t))

#4 Class inside class
class Battery:
    capacity = "4000mAh"

class Smartphone:
    battery = Battery()

s = Smartphone()
print(s.battery.capacity)

#5 Class with attribute that is a number
class Circle:
    radius = 7

c = Circle()
print(c.radius)