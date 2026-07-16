from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.teleport(0, 270)
        self.color("white")
        self.hideturtle()

    def update(self):
        self.write(f"Score: {self.score}", False, "center", ("Courier", 22, "normal"))

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update()

    def game_over(self):
        self.teleport(0, 0)
        self.write("Game Over", False, "center", ("Courier", 22, "normal"))