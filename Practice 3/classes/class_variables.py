# 1
class Dog:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name

dog1 = Dog("Buddy")
dog2 = Dog("Max")

print(dog1.species)
print(dog2.species)


# 2
class User:
    user_count = 0

    def __init__(self, username):
        self.username = username
        User.user_count += 1


u1 = User("alice")
u2 = User("bob")

print(User.user_count)


# 3
class Car:
    wheels = 4

    def __init__(self, brand):
        self.brand = brand


car1 = Car("Toyota")
car2 = Car("BMW")

car1.wheels = 6

print(car1.wheels)
print(car2.wheels)
print(Car.wheels)


# 4
class Counter:
    count = 0  

    def __init__(self):
        Counter.count += 1


a = Counter()
b = Counter()

print(Counter.count)
