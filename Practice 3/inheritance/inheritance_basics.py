# 1
class Animal:
    def speak(self):
        print("Animal sound")


class Dog(Animal):
    pass

dog = Dog()
dog.speak()


# 2
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    pass

s = Student("Alice")
print(s.name)


# 3     
class Vehicle:
    wheels = 0


class Bike(Vehicle):
    wheels = 2

print(Bike.wheels)


# 4
class Shape:
    def area(self):
        return 0


class Square(Shape):
    pass


sq = Square()
print(sq.area())
