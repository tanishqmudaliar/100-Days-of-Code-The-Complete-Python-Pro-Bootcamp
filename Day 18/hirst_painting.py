from turtle import Turtle, Screen, colormode
from extract_colors import extract_colors

color_list = extract_colors()
colormode(255)

main_axis_x = -225
main_axis_y = -225

timmy = Turtle()
screen = Screen()
screen.setup(1.0,1.0)
timmy.speed("fastest")
timmy.teleport(main_axis_x, main_axis_y)

def change_color(x):
    timmy.color(color_list[x])

def draw(times):
    color = 0
    y_axis = main_axis_y
    for j in range(times):
        x_axis = main_axis_x
        for i in range(times):
            change_color(color)
            timmy.begin_fill()
            timmy.circle(20)
            timmy.end_fill()
            if color == 29:
                color = 0
            else:
                color += 1
            if i < times - 1:
                x_axis += 50
            else:
                x_axis = main_axis_x
            timmy.teleport(x_axis, y_axis)
        if j < times - 1:
            y_axis += 50
        else:
            y_axis = main_axis_y
        timmy.teleport(x_axis, y_axis)

timmy.showturtle()
draw(10)
timmy.hideturtle()

screen.exitonclick()
