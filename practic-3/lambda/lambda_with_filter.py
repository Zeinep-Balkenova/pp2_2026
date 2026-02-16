nums = [1, 2, 3, 4]
evens = list(filter(lambda x: x % 2 == 0, nums))

nums = [-1, 0, 2]
positive = list(filter(lambda x: x > 0, nums))

words = ["hi", "hello"]
long = list(filter(lambda w: len(w) > 2, words))

ages = [12, 18, 20]
adult = list(filter(lambda x: x >= 18, ages))

data = ["", "text"]
filled = list(filter(lambda x: x, data))
