from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.teleport(-100, 200)
        self.write(self.l_score, align="center", font=("Courier", 88, "normal"))
        self.teleport(100, 200)
        self.write(self.r_score, align="center", font=("Courier", 88, "normal"))

    def l_point(self):
        self.l_score += 1

    def r_point(self):
        self.r_score += 1