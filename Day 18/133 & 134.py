from turtle import Turtle, Screen, colormode
import random

colormode(255)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r,g,b

timmy = Turtle()
screen = Screen()

def random_walk(iterations):
    timmy.pensize(10)
    timmy.speed("fastest")
    for _ in range(iterations):
        timmy.color(random_color())
        timmy.setheading(random.choice([0, 90, 180, 270]))
        timmy.forward(20)

random_walk(300)