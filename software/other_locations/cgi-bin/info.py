#!/usr/bin/python3

with open("/home/pi/co2/software/values_with_window.csv", "r") as file:
    contents = file.read().split("\n")

print("Content-type: text/html\n\n")
print("CO2: ",int(float(contents[-2].split(";")[1])))
