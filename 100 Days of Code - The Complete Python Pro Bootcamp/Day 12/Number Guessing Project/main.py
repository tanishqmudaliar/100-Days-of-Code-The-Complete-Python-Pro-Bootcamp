import random
from art import logo

print(logo)
print("Welcome to the number guessing game!")
print("I'm thinking of a number between 1 and 100.")

difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
if difficulty == "easy":
    lives = 10
elif difficulty == "hard":
    lives = 5
else:
    print("Sorry, that's not a valid difficulty.")
    raise SystemExit

predicted_number = random.randint(1, 100)
game_over = False

while not game_over:
    guess = int(input("Make a guess: "))
    if guess == predicted_number:
        print(f"You got it! The answer was {predicted_number}.")
        game_over = True
    elif guess > predicted_number:
        print("You guessed too high.")
        lives -= 1
    else:
        print("You guessed too low.")
        lives -= 1

    if not game_over:
        if lives == 0:
            print("You've run out of guesses, you lose.")
            game_over = True
        else:
            print("Guess again.")
            print(f"You have {lives} attempts remaining to guess the number.")