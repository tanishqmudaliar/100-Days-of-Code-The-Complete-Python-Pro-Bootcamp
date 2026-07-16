import random
from turtle import Turtle, Screen

is_race_on = False

screen = Screen()
screen.setup(width=500, height=400)

user_bet = None

while user_bet is None:
    user_bet = screen.textinput(
        title="Make your bet",
        prompt="Which turtle will win the race? Choose a color (red/orange/yellow/green/blue/purple): "
    )

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtles = []

for color in colors:
    t = Turtle(shape="turtle")
    t.color(color)
    t.penup()
    turtles.append(t)

y = -100
for turtle in turtles:
    turtle.goto(-230, y)
    y += 40

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in turtles:
        turtle.forward(random.randint(1, 10))

        if turtle.xcor() >= 230:
            winner = turtle.pencolor()
            is_race_on = False

            if winner.lower() == user_bet.lower():
                print(f"You've won! The {winner} turtle won the race!")
            else:
                print(f"You've lost. The {winner} turtle won the race!")

            break

# screen.exitonclick()