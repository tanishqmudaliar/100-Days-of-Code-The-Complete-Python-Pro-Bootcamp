import random

num = random.randint(1, 10)
if num % 2 == 0:
    print(num)
    print("Heads")
else:
    print(num)
    print("Tails")