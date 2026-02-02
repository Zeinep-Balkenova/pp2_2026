for i in range(1, 6):
    if i == 3:
        continue
    print(i)

for i in range(6):
    if i % 2 == 0:
        continue
    print(i)

words = ["yes", "", "no"]
for word in words:
    if word == "":
        continue
    print(word)

for char in "banana":
    if char == "a":
        continue
    print(char)

numbers = [1, -2, 3, -4]
for n in numbers:
    if n < 0:
        continue
    print(n)
