#!/usr/bin/python3

import time
import motor
import datetime
import traceback

is_open = False
previous_co2_value = 2000
previous2_co2_value = 2000
co2_value = 2000

while True:
	
	time.sleep(30)
	upper_threshold = 2000			# if co2 is larger, open window
	lower_threshold = 1350			# if co2 is lower, close window
	preliminary_threshold = 1700    # if co2 is higher at 5:00 am, open window (until max. 5:45 am)
	
	# open window from 20:00 pm to 20:30 pm
	
	
	# read current co2 value
	try:
		filename = "/home/pi/co2/software/values.csv"
		with open(filename, "r") as file:
			contents = file.read()
			previous2_co2_value = previous_co2_value
			previous_co2_value = co2_value
			last_line = contents.split("\n")[-2]
			t, co2_value, brightness = last_line.split(";")
			t = float(t)
			brightness = float(brightness)
			co2_value = float(co2_value)
			increment = co2_value - previous2_co2_value
			
			state = "open" if is_open else "closed"
			print(f"{datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')} " \
			    f"{co2_value} ppm ({increment:+0.0f}), brightness: {brightness:.3f}, window is {state}")
	except:
		traceback.print_exc()
		pass
		
	now = datetime.datetime.now()
	allow_open = now.hour > 12 or now.hour <= 5 or (now.hour == 5 and now.minute <= 45)
	
	if not is_open and allow_open:
		if co2_value >= upper_threshold \
			or (now.hour == 5 and co2_value >= preliminary_threshold) \
			or (now.hour == 20 and 0 <= now.minute <= 2):
			
			print(f"co2_value ({co2_value}), upper_threshold ({upper_threshold}), allow_open: {allow_open} -> open window")
			motor.turn_open()
			is_open = True
		
	if is_open:
		if co2_value <= lower_threshold or not allow_open \
			or (now.hour == 20 and 30 <= now.minute <= 35):

			print(f"co2_value ({co2_value}), lower_threshold ({lower_threshold}), allow_open: {allow_open} -> close window")
			motor.turn_close()
			is_open = False
