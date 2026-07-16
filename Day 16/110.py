from turtle import Turtle, Screen
timmy = Turtle()
screen = Screen()

timmy.shape("turtle")
timmy.color("DarkGoldenrod1")
timmy.forward(100)
timmy.left(90)
timmy.forward(100)

my_screen = Screen()
my_screen.exitonclick()

print(timmy, my_screen)