from turtle import Turtle, Screen

timmy = Turtle()
screen = Screen()

def move_forward():
    timmy.forward(10)

def move_backward():
    timmy.backward(10)

def tilt_left():
    timmy.left(10)

def tilt_right():
    timmy.right(10)

def clear_screen():
    timmy.reset()

screen.listen()
screen.onkeypress(move_forward, "w")
screen.onkeypress(move_backward, "s")
screen.onkeypress(tilt_left, "a")
screen.onkeypress(tilt_right, "d")
screen.onkeypress(clear_screen, "c")
screen.exitonclick()