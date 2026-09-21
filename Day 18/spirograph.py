from turtle import Turtle, Screen, colormode
import random

def random_color():
    colormode(255)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r,g,b

timmy = Turtle()
screen = Screen()

def draw_circle():
    angle = 0
    timmy.speed("fastest")
    for _ in range(180):
        timmy.color(random_color())
        timmy.circle(100)
        angle -= 2
        timmy.setheading(angle)

draw_circle()
screen.exitonclick()