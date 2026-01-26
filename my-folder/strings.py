#Example
#Strings in python are surrounded by either single quotation marks, or double quotation marks.
print("Hello")
print('Hello')

#Example 
#Quotes Inside Quotes
#You can use quotes inside a string, as long as they don't match the quotes surrounding the string:
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

#Example
#You can use three double quotes:
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
#or 
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

#Example
a = "Hello"
print(a)

#Get the character at position 1 (remember that the first character has the position 0):
a = "Hello, World!"
print(a[1])

#Example
#Loop through the letters in the word "banana":
for x in "banana":
  print(x)

#Example
#The len() function returns the length of a string:
a = "Hello, World!"
print(len(a))

#Example
#Check if "free" is present in the following text:
txt = "The best things in life are free!"
print("free" in txt)

#Example
#Get the characters from position 2 to position 5 (not included):
b = "Hello, World!"
print(b[2:5])

#Example
#Get the characters from the start to position 5 (not included):
b = "Hello, World!"
print(b[:5])

#Example
#Get the characters from position 2, and all the way to the end:
b = "Hello, World!"
print(b[2:])

#Example
#The strip() method removes any whitespace from the beginning or the end:
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#Example
#The replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J"))

#Example
#The split() method splits the string into substrings if it finds instances of the separator:
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

#Example
#The escape character allows you to use double quotes when you normally would not be allowed:
txt = "We are the so-called \"Vikings\" from the north."





