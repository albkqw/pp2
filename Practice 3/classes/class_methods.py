# 1
class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("Rex")
dog2 = Dog("Nif")
print(dog1.name)
print(dog2.name)


# 2
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
s1 = Student("Alibek", 18)
print(s1.name, s1.grade)


# 3
class Car:
    def __init__(self, brand):
        self.brand = brand

    def drive(self):
        print(f"{self.brand} is driving!")
car1 = Car("Ferrari")
car1.drive()


# 4
class School:
    school_name = "High School"   # class variable

    def __init__(self, student):
        self.student = student    # instance variable

s1 = School("Ali")
s2 = School("Dana")

print(s1.school_name)
print(s2.school_name)

s1.school_name = "New School"

print(s1.school_name)
print(s2.school_name)
print(School.school_name)
