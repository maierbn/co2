
import RPi.GPIO as GPIO
import time

pin_shutter_close = 11
pin_shutter_open = 16

def close_shutter():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin_shutter_close, GPIO.OUT)
  GPIO.output(pin_shutter_close, GPIO.LOW)
  time.sleep(1)
  GPIO.cleanup(pin_shutter_close)

def open_shutter():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin_shutter_open, GPIO.OUT)
  GPIO.output(pin_shutter_open, GPIO.LOW)
  time.sleep(1)
  GPIO.cleanup(pin_shutter_open)

