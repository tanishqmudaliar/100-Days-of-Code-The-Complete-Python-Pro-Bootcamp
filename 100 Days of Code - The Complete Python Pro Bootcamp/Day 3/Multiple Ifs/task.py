print("Welcome to the rollercoaster!")
height = int(input("What is your height in cm? "))
bill = 0

if height >= 120:
    print("You can ride the rollercoaster")
    age = int(input("What is your age? "))
    if age <= 12:
        bill = 5
    elif age <= 18:
        bill = 7
    else:
        bill = 12

    wants_photo = bool(input("Do you want a  photo? type True for yes and False for no"))
    if wants_photo == True:
        bill = bill + 3

    print(f"Your total bill = ${bill}")

else:
    print("Sorry you have to grow taller before you can ride.")
