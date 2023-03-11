#!/usr/bin/python3

with open("command", "w") as file:
    file.write("open_shutter")

print("Content-type: text/html\n\nopen_shutter")
