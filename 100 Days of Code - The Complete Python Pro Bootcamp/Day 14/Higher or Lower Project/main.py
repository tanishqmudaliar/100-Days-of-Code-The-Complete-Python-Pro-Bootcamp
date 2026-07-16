from art import logo, vs
from game_data import data
import random

def game(personOne, personTwo, score):
    print(logo)
    if score > 0:
        print(f"You're right! Current score: {score}.")
    print(f"Compare A: {personOne["name"]}, {personOne["description"]} from {personOne["country"]}.")
    print(vs)
    print(f"Against B: {personTwo["name"]}, {personTwo["description"]} from {personTwo["country"]}.")
    decision = input("Who has more followers? Type 'A' or 'B': ").upper()
    if personOne["follower_count"] > personTwo["follower_count"]:
        correct_answer = 'A'
    else:
        correct_answer = 'B'
    if decision == correct_answer:
        print("You are right!")
        return personTwo
    else:
        print(logo,"\nSorry, that's wrong.")
        return "game over"

person_one = random.choice(data)
person_two = random.choice(data)
while person_one == person_two:
    person_two = random.choice(data)
gameover = False
current_score = 0
while not gameover:
    winner = game(person_one, person_two, current_score)
    if winner == "game over":
        gameover = True
    else:
        person_one = winner
        person_two = random.choice(data)
        while person_one == person_two:
            person_two = random.choice(data)
        current_score += 1
