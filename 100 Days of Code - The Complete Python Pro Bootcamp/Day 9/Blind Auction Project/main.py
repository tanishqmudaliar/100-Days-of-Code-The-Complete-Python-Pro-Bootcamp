# TODO-1: Ask the user for input
# TODO-2: Save data into dictionary {name: price}
# TODO-3: Whether if new bids need to be added
# TODO-4: Compare bids in dictionary
from art import logo

bids = {}
bidding_finished = False

print(logo)

def bid():
    name = input("What is your name?: ")
    price = int(input("What is your bid?: $"))
    bids[name] = price

bid()

while not bidding_finished:
    decision = input("Are there any other bidders? Type 'yes' or 'no'.").lower()
    if decision == "yes":
        print("\n" * 100)
        bid()
    elif decision == "no":
        print("\n" * 100)
        bidding_finished = True
        for bid in bids:
            highest_bid = 0
            winner = ""
            if bids[bid] > highest_bid:
                highest_bid = bids[bid]
                winner = bid
        print(f"The highest bid is ${highest_bid} by {winner}")
    else:
        print("Sorry, I didn't understand that.")