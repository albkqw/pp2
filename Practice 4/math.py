import math

# 1
degree = int(input("Input degree: "))
radian = degree * (math.pi / 180)
print(radian)


# 2
h = int(input("Input height: "))
a = int(input("Input first base: "))
b = int(input("Input second base: "))
print((a+b)/2 * h)


# 3
n = int(input("Input number of sides: "))
a = int(input("Input the length of a side: "))
area = (n * a**2) / (4 * math.tan(math.pi / n))
print(round(area))


# 4
base = int(input("Length of base: "))
height = int(input("Height of parallelogram: "))
area = base * height
print(float(area))


