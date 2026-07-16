from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

while True:
    choice = input("What would you like? (espresso/latte/cappuccino/):")

    if choice in ["espresso", "latte", "cappuccino"]:
        drink = menu.find_drink(choice)

        if coffee_maker.is_resource_sufficient(drink):
            if money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)

    elif choice == "report":
        coffee_maker.report()
        money_machine.report()

    elif choice == "off":
        break

    else:
        print(f"Invalid choice. We only have {menu.get_items()}.")