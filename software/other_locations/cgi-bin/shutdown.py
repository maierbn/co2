#!/usr/bin/python3

with open("command", "w") as file:
    file.write("shutdown")

print("Content-type: text/html\n\nshutdown")
