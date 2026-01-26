#Example
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#Example
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#Example
x = y = z = "Orange"
print(x)
print(y)
print(z)

#Create a variable outside of a function, and use it inside the function

x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
