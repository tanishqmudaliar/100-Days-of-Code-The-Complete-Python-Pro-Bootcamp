import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n"))
if choice == 0:
    print(f"{rock}\nComputer chose:")
    computerChoice = random.randint(0,2)
    if computerChoice == 0:
        print(f"{rock}\nIt's a draw.")
    elif computerChoice == 1:
        print(f"{paper}\nYou lose.")
    elif computerChoice == 2:
        print(f"{scissors}\nYou win!")
elif choice == 1:
    print(f"{paper}\nComputer chose:")
    computerChoice = random.randint(0, 2)
    if computerChoice == 0:
        print(f"{rock}\nYou win!")
    elif computerChoice == 1:
        print(f"{paper}\nIt's a draw.")
    elif computerChoice == 2:
        print(f"{scissors}\nYou lose.")
elif choice == 2:
    print(f"{scissors}\nComputer chose:")
    computerChoice = random.randint(0, 2)
    if computerChoice == 0:
        print(f"{rock}\nYou lose.")
    elif computerChoice == 1:
        print(f"{paper}\nYou win!")
    elif computerChoice == 2:
        print(f"{scissors}\nIt's a draw.")
else:
    print("You typed an invalid number, you lose!")