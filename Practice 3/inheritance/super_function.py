# 1
class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)  # call parent constructor


dog = Dog("Buddy")
print(dog.name)


# 2
class A:
    def hello(self):
        print("Hello from A")


class B(A):
    def hello(self):
        super().hello()  # call parent method
        print("Hello from B")


b = B()
b.hello()


# 3
class Parent:
    value = 10


class Child(Parent):
    def show(self):
        print(super().value)  # access parent attribute


c = Child()
c.show()


# 4
class Base:
    def info(self):
        print("Base class")


class Derived(Base):
    def info(self):
        super().info()
        print("Derived class")


d = Derived()
d.info()
