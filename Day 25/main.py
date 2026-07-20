from turtle import Screen, Turtle

import pandas

screen = Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
screen.setup(width=478, height=561)
map_turtle = Turtle()
map_turtle.shape(image)
map_turtle.penup()

writer = Turtle()
writer.hideturtle()
writer.penup()

states_guessed = 0
states = 28

data = pandas.read_csv("28_states.csv")

while states_guessed < states:
    if states_guessed == 0:
        answer_state = screen.textinput(title="Answer the state", prompt="What's another state's name?")
    else:
        answer_state = screen.textinput(title=f"{states_guessed}/{states}", prompt="What's another state's name?")

    for state in data.state:
        if answer_state.lower() == state.lower():
            states_guessed += 1

            state_data = data[data.state.str.lower() == answer_state.lower()]

            x = state_data.x.iloc[0]
            y = state_data.y.iloc[0]

            writer.goto(x, y)
            writer.write(state, align="center", font=("Arial", 10, "normal"))

            data = data[data.state.str.lower() != answer_state.lower()]
            break

    if answer_state == "exit":
        pandas.DataFrame(data.state).to_csv("missing_states.csv")
        break