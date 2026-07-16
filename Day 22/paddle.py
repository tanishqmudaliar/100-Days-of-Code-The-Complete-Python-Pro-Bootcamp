from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, pos):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()

        if pos == "left":
            self.goto(-375, 0)
        elif pos == "right":
            self.goto(375, 0)

    def up(self):
        if self.ycor() < 275:
            self.sety(self.ycor() + 20)

    def down(self):
        if self.ycor() > -275:
            self.sety(self.ycor() - 20)