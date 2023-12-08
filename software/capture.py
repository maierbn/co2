#!/usr/bin/python3


import sys
import os
import datetime
import timeit
import time
import numpy as np
import cv2

output_directory = "/home/pi/co2/software/output"
interval = 30 		# [s]

def get_brightness(filename):
	im = cv2.imread(filename)

	# calculate mean value from RGB channels and flatten to 1D array
	values = im.mean(axis=2).flatten()
	
	brightness = np.mean(values)
	return brightness/255.
	
# open sensor handle
import cozir
co2_sensor = cozir.Cozir('/dev/ttyUSB0')

# camera
if False:
	import picamera
	camera = picamera.PiCamera()
	camera.resolution = (1920,1080)
	camera.exposure_mode = "night"
	camera.awb_mode = "shade"
	camera.image_effect = "none"
	camera.contrast =    50  # 0 to 100
	camera.brightness =  70 # 0 to 100
	camera.annotate_background = picamera.Color('white')
	camera.annotate_foreground = picamera.Color('black')

while True:
	
	tstart = timeit.default_timer()
	now = datetime.datetime.now()
	
	# capture current ppm value of CO2 concentration
	try:
		co2_value = co2_sensor.read_CO2()
	except:
		pass
    
	# take picture with camera
	#camera.annotate_text = "{} CO2: {} ppm".format(
	#	now.strftime("%d.%m.%Y %H:%M:%S"), co2_value)

	#filename = os.path.join(output_directory, "{}.jpg".format(now.timestamp()))
	#camera.capture(filename)

	# determine brihgtness
	#brightness = get_brightness(filename)
	brightness = 0
	
	# remove image
	try:
		os.remove(filename)
	except:
		pass
	

	# take video with camera
	#filename = os.path.join(output_directory, "video.h264")
	#camera.start_recording(filename)
	#time.sleep(10)
	#camera.stop_recording()
	#print("recording finished")
	

	print(f"{now.strftime('%H:%M:%S')} {co2_value} ppm, brightness: {brightness:.3f}")

	# dump values to log file
	with open("values.csv", "a") as file:
		file.write(f"{now.timestamp()};{co2_value};{brightness} \n")
    
	# sleep
	tstop = timeit.default_timer()
	time.sleep(interval - (tstop - tstart))
  
