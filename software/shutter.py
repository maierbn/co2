
import RPi.GPIO as GPIO
import time

pin_shutter_close = 17
pin_shutter_open = 23

def close_shutter():
  print("close shutter")
  #return
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_shutter_close, GPIO.OUT)
  GPIO.output(pin_shutter_close, GPIO.LOW)
  time.sleep(1)
  GPIO.cleanup(pin_shutter_close)

def open_shutter():
  print("open shutter")
  #return 
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_shutter_open, GPIO.OUT)
  GPIO.output(pin_shutter_open, GPIO.LOW)
  time.sleep(1)
  GPIO.cleanup(pin_shutter_open)

