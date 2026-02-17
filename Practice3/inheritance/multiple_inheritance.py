#1 Basic multiple inheritance
class A:
    def method_a(self):
        print("A method")

class B:
    def method_b(self):
        print("B method")

class C(A, B):
    pass

c = C()
c.method_a()
c.method_b()

#2 Multiple inheritance with attributes
class X:
    x = 5

class Y:
    y = 10

class Z(X, Y):
    pass

z = Z()
print(z.x, z.y)

#3 Multiple inheritance with methods
class Parent1:
    def hello(self):
        print("Hello from Parent1")

class Parent2:
    def bye(self):
        print("Goodbye from Parent2")

class Child(Parent1, Parent2):
    pass

child = Child()
child.hello()
child.bye()

#4 Multiple inheritance overriding method
class Base1:
    def greet(self):
        print("Hi from Base1")

class Base2:
    def greet(self):
        print("Hi from Base2")

class Derived(Base1, Base2):
    pass

Derived().greet()

#5 Multiple inheritance with constructor
class P1:
    def __init__(self):
        print("P1 init")

class P2:
    def __init__(self):
        print("P2 init")

class C(P1, P2):
    def __init__(self):
        P1.__init__(self)
        P2.__init__(self)
        print("C init")

C()