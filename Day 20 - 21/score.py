from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt", mode="a"):
            pass
        with open("data.txt", mode="r") as file:
            data = file.read()
            if data == "":
                self.highscore = 0
            else:
                self.highscore = int(data)
        self.penup()
        self.teleport(0, 270)
        self.color("white")
        self.hideturtle()

    def update(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.highscore}", False, "center", ("Courier", 22, "normal"))

    def increase_score(self):
        self.score += 1
        self.update()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", "w") as file:
                file.write(str(self.highscore))
        self.score = 0
        self.update()