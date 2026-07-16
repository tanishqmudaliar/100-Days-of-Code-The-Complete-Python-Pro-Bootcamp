MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 900,
    "milk": 600,
    "coffee": 300,
    "money": 0,
}

machineOn = True

def report():
    """Prints a report of all resources."""
    print(f"Water: {resources['water']}ml\nMilk: {resources['milk']}ml\nCoffee: {resources['coffee']}g\nMoney: ${resources['money']}")

def checkResources(drink):
    """Checks if there are enough resources to make the drink."""
    item_not_available = []
    for item in MENU[drink]["ingredients"]:
        if MENU[drink]["ingredients"][item] > resources[item]:
            item_not_available.append(item)
    if not item_not_available:
        processCoins(drink)
    else:
        print(f"Sorry there is not enough {item_not_available[0]}.")

def processCoins(drink):
    """Processes the coins inserted by the user."""
    print("Please insert coins.")
    try:
        quarters = int(input("How many quarters?: ")) * 0.25
        dimes = int(input("How many dimes?: ")) * 0.10
        nickels = int(input("How many nickels?: ")) * 0.05
        pennies = int(input("How many pennies?: ")) * 0.01
        total = quarters + dimes + nickels + pennies
        cost = MENU[drink]["cost"]
        if total < cost:
            print("Sorry that's not enough money. Money refunded.")
        else:
            change = round(total - cost, 2)
            if change > 0:
                print(f"Here is ${change} in change.")
            resources["money"] += cost
            makeDrink(drink)
    except ValueError:
        print("Invalid input. Please enter numeric values for coins.")

def makeDrink(drink):
    """Deducts the required ingredients from the resources."""
    for item in MENU[drink]["ingredients"]:
        resources[item] -= MENU[drink]["ingredients"][item]
    print(f"Here is your {drink} ☕️. Enjoy!")

def main():
    """Main function to run the coffee machine."""
    global machineOn, resources
    choice = input("What would you like? (espresso/latte/cappuccino): ")
    if choice == "off":
        machineOn = False
        return
    elif choice == "report":
        report()
    elif choice in ["latte", "cappuccino", "espresso"]:
        checkResources(choice)
    else:
        print("Invalid selection. Please choose again.")

while machineOn:
    main()