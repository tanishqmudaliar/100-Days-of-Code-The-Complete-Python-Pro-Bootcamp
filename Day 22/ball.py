from random import randint, choice
from turtle import Turtle

MOVE_DISTANCE = 5

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.reset_ball(choice([True, False]))

    def move(self):
        self.forward(MOVE_DISTANCE)

    def bounce_y(self):
        self.setheading(360 - self.heading())

    def bounce_x(self):
        self.setheading((180 - self.heading()) % 360)

    def reset_ball(self, reset_choice):
        self.goto(0, 0)

        if reset_choice:
            self.setheading(randint(-45, 45))
        else:
            self.setheading(randint(135, 225))