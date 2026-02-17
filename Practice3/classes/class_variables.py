#1 Shared class variable
class School:
    name = "NIS"

s1 = School()
s2 = School()
print(s1.name, s2.name)

#2 Changing class variable
class Game:
    players = 0

Game.players += 2
print(Game.players)

#3 Class variable accessed from object
class Country:
    continent = "Asia"

c = Country()
print(c.continent)

#4 Class variable and instance variable
class Animal:
    type = "Mammal"
    
    def __init__(self, name):
        self.name = name

a = Animal("Dog")
print(a.name, a.type)

#5 Class variable used in method
class Math:
    factor = 2
    
    def multiply(self, x):
        return x * Math.factor

m = Math()
print(m.multiply(5))