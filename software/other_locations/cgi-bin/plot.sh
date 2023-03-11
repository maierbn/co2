#!/bin/bash

echo Content-type: text/html
echo
cd /home/pi/co2/software/
/usr/bin/python3 ./plot.py
echo plot created
