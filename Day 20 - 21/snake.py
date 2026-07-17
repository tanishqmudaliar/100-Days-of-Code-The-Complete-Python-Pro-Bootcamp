from turtle import Turtle
class Snake:
    def __init__(self):
        self.delay_speed = 0.2
        self.snakes = []
        self.position = 3
        self.snake(self.position)
        self.head = self.snakes[0]

    def extend(self, i=None):
        t = Turtle("square")
        t.color("white")
        t.penup()

        if i is not None:
            # Initial snake creation
            t.goto(-20 * i, 0)
        else:
            # Add new segment at the tail
            tail = self.snakes[-1]
            t.goto(tail.position())

        self.snakes.append(t)

    def snake(self, position):
        for i in range(position):
            self.extend(i)

    def up(self):
        if self.snakes[0].heading() != 270:
            self.snakes[0].setheading(90)

    def down(self):
        if self.snakes[0].heading() != 90:
            self.snakes[0].setheading(270)

    def left(self):
        if self.snakes[0].heading() != 0:
            self.snakes[0].setheading(180)

    def right(self):
        if self.snakes[0].heading() != 180:
            self.snakes[0].setheading(0)

    def move(self):
        for i in range(len(self.snakes) - 1, 0, -1):
            x = self.snakes[i - 1].xcor()
            y = self.snakes[i - 1].ycor()
            self.snakes[i].goto(x, y)

        self.snakes[0].forward(20)
        self.head = self.snakes[0]

    def reset(self):
        for seg in self.snakes:
            seg.goto(1000, 1000)
        self.snakes.clear()
        self.snake(self.position)
        self.head = self.snakes[0]