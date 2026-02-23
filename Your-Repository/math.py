"""Write a Python program to convert degree to radian.
Input degree: 15
Output radian: 0.261904"""

degree = float(input())
pi = 22 / 7
radian = degree * pi / 180
print(f"radian: {radian:.6f}")


"""Write a Python program to calculate the area of a trapezoid.
Height: 5
Base, first value: 5
Base, second value: 6
Expected Output: 27.5"""

height = float(input("Height: "))
base1 = float(input("Base, first: "))
base2 = float(input("Base, second: "))
area = (base1 + base2) / 2 * height
print(area)


"""Write a Python program to calculate the area of regular polygon.
Input number of sides: 4
Input the length of a side: 25
The area of the polygon is: 625"""

import math

n = int(input("sides: "))
side = float(input("length: "))
area = (n * side ** 2) / (4 * math.tan(math.pi / n))
print(area)


"""Write a Python program to calculate the area of a parallelogram.
Length of base: 5
Height of parallelogram: 6
Expected Output: 30.0"""

base = float(input("Length: "))
height = float(input("Height: "))

area = base * height

print(area)


