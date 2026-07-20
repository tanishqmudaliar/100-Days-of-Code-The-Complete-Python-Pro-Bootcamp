import pandas

data = pandas.read_csv("squirrel.csv")

gray = 0
cinnamon = 0
black = 0
for squirrel in data["Primary Fur Color"]:
    if squirrel == "Black":
        black += 1
    elif squirrel == "Cinnamon":
        cinnamon += 1
    elif squirrel == "Gray":
        gray += 1

new_data = {
    "Fur Color" : ["Gray", "Cinnamon", "Black"],
    "Count" : [gray, cinnamon, black]
}

pandas.DataFrame(new_data).to_csv("squirrel_count.csv")