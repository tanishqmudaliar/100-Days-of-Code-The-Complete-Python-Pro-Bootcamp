import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from score import Score

screen = Screen()
screen.setup(width=800, height=650)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

left_paddle = Paddle("left")
right_paddle = Paddle("right")
ball = Ball()
score = Score()

screen.listen()

screen.onkeypress(left_paddle.up, "w")
screen.onkeypress(left_paddle.up, "W")
screen.onkeypress(left_paddle.down, "s")
screen.onkeypress(left_paddle.down, "S")

screen.onkeypress(right_paddle.up, "Up")
screen.onkeypress(right_paddle.down, "Down")

game_is_on = True
delay = 0.02

while game_is_on:
    time.sleep(delay)
    screen.update()
    ball.move()

    if ball.ycor() >= 315 or ball.ycor() <= -315:
        ball.bounce_y()

    if (
        ball.xcor() >= 355
        and ball.distance(right_paddle) <= 50
    ):
        ball.bounce_x()
        if delay > 0.005:
            delay *= 0.90

    if (
        ball.xcor() <= -355
        and ball.distance(left_paddle) <= 50
    ):
        ball.bounce_x()
        if delay > 0.005:
            delay *= 0.90

    if ball.xcor() > 380:
        ball.reset_ball(False)
        score.l_point()
        delay = 0.02

    if ball.xcor() < -380:
        ball.reset_ball(True)
        score.r_point()
        delay = 0.02

    score.update_score()
    print(f"{delay:.10f}")

screen.exitonclick()