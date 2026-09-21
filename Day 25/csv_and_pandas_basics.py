with open("weather_data.csv") as weather_data:
    data = weather_data.readlines()
    print(data)

import csv

with open("weather_data.csv") as csvfile:
    data = csv.reader(csvfile)
    temperatures = []
    for row in data:
        if row[1] != "temp":
            temperatures.append(int(row[1]))
    print(temperatures)

import pandas

data = pandas.read_csv("weather_data.csv")

temps = data["temp"].to_list()
avg_temp = 0
for temp in temps:
    avg_temp = avg_temp + temp
avg_temp = avg_temp / len(temps)
print(round(avg_temp))

data_dict = data.to_dict()
print(data_dict)

temp_list = data["temp"].to_list()
print(len(temp_list))

max_temp = data["temp"].max()
print(max_temp)

print(data[data.day == "Monday"])

print(data[data.temp == data.temp.max()])

monday = data[data.day == "Monday"]
print(monday.condition)

monday_temp = monday.temp
monday_tempF = monday_temp * 9/5 + 32

print(monday_tempF)

