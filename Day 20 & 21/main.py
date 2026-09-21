import time
from turtle import Screen
from score import Score
from snake import Snake
from food import Food

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Snake II")
screen.tracer(0)

snake = Snake()
food = Food()
score = Score()
score.update()

screen.listen()

screen.onkey(snake.up, "w")
screen.onkey(snake.up, "W")
screen.onkey(snake.up, "Up")

screen.onkey(snake.down, "s")
screen.onkey(snake.down, "S")
screen.onkey(snake.down, "Down")

screen.onkey(snake.left, "a")
screen.onkey(snake.left, "A")
screen.onkey(snake.left, "Left")

screen.onkey(snake.right, "d")
screen.onkey(snake.right, "D")
screen.onkey(snake.right, "Right")

game_is_on = True
iterations = 0

while game_is_on:
    screen.update()
    time.sleep(snake.delay_speed)

    snake.move()

    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        score.increase_score()
        if iterations == 9:
            iterations = 0
            snake.delay_speed -= 0.025
        else:
            iterations += 1

    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        score.reset()
        snake.reset()

    for parts in snake.snakes[1:]:
        if snake.head.distance(parts) < 10:
            score.reset()
            snake.reset()

screen.exitonclick()