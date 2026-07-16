import random
from art import logo

cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def calculate_score(hand):
    score = 0
    aces = hand.count("A")

    for card in hand:
        if card == "A":
            score += 11
        else:
            score += card

    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score


def game():
    print(logo)
    your_cards = [random.choice(cards), random.choice(cards)]
    computer_cards = [random.choice(cards), random.choice(cards)]

    game_over = False

    while not game_over:
        your_score = calculate_score(your_cards)

        print(f"\nYour cards: {your_cards} | score: {your_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if your_score == 21:
            print("Blackjack! You win 😎")
            return

        if your_score > 21:
            print("You went over. You lose 😤")
            return

        choice = input("Type 'y' to draw another card, 'n' to pass: ")

        if choice == "y":
            your_cards.append(random.choice(cards))
        else:
            game_over = True

    while calculate_score(computer_cards) < 17:
        computer_cards.append(random.choice(cards))
        print(f"Computer draws a card: {computer_cards[-1]}")

    your_score = calculate_score(your_cards)
    computer_score = calculate_score(computer_cards)

    print("\nFinal hands:")
    print(f"Your cards: {your_cards} | final score: {your_score}")
    print(f"Computer cards: {computer_cards} | final score: {computer_score}")

    if computer_score > 21:
        print("Computer went over. You win 😃")
    elif your_score > computer_score:
        print("You win 😃")
    elif your_score < computer_score:
        print("You lose 😭")
    else:
        print("It's a draw 🙃")

while True:
    play = input("\nDo you want to play a game of Blackjack? (y/n): ")
    if play == "y":
        game()
    else:
        print("Game Over 👋")
        break
