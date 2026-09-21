from turtle import Turtle, Screen, colormode
import random

colormode(255)

timmy = Turtle()
screen = Screen()

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r,g,b

def draw_shapes(length, angle, sides):
    timmy.color(random_color())
    for i in range(sides):
        timmy.forward(length)
        timmy.right(angle)

draw_shapes(100, 120,3)
draw_shapes(100, 90, 4)
draw_shapes(100, 72, 5)
draw_shapes(100, 60, 6)
draw_shapes(100, 51.43, 7)
draw_shapes(100, 45, 8)
draw_shapes(100, 40, 9)
draw_shapes(100, 36, 10)

screen.exitonclick()