from art import logo

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

def ask(start, answer):
    if start is not True:
        num1 = answer
    else:
        num1 = int(input("Enter a number: "))
    num2 = int(input("Enter another number: "))
    op = input("Pick an operation (+, -, *, /): ")
    return num1, num2, op

over = False
print(logo)

start = True
answer = 0

while not over:
    result = ask(start, answer)

    if result[2] == "+":
        answer = add(result[0], result[1])
    elif result[2] == "-":
        answer = subtract(result[0], result[1])
    elif result[2] == "*":
        answer = multiply(result[0], result[1])
    elif result[2] == "/":
        answer = divide(result[0], result[1])
    else:
        print("Invalid operation.")
        continue

    print(round(answer))

    decision = input("Do you want to continue? (y/n): ")
    if decision == "y":
        start = False   # reuse answer next loop
    else:
        over = True
