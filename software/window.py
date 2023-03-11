#!/usr/bin/python3

import time
import motor
import shutter
import datetime
import traceback
import subprocess

is_open = False
previous_co2_value = 2000
previous2_co2_value = 2000
co2_value = 2000
log_filename = "/home/pi/co2/software/log_window.txt"
long_log_filename = "/home/pi/co2/software/values_with_window.csv"
command_filename = "/home/pi/co2/software/command"

forced_open = False
forced_close = False
forced_end_time = datetime.datetime.now()
enabled = True

# main loop
while True:
  
  time.sleep(30)
  upper_threshold = 2000      # if co2 is larger, open window
  lower_threshold = 1350      # if co2 is lower, close window
  preliminary_threshold = 1700    # if co2 is higher at 5:00 am, open window (until max. 5:45 am)
  
  if forced_end_time < datetime.datetime.now():
    forced_open = False
    forced_close = False

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
          
    # own log file
    with open(long_log_filename, "a") as file:
      file.write(f"{datetime.datetime.now().timestamp()};{co2_value};{brightness};{state} \n")
  except:
    traceback.print_exc()
    pass
    
  # check for command
  with open(command_filename, "r") as file:
    command = file.read()

    if command != "":
      # write message to log
      with open(log_filename, "a") as file:
        file.write(f"{datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')} " \
          f"{co2_value} ppm ({increment:+0.0f}), brightness: {brightness:.3f}, window is {state}, command {command}\n")
        print(f"Command {command}")
   
      # clear command
      with open(command_filename, "w") as file:
        file.write("")

    # handle parsed command
    if command == "open" and not is_open and enabled:
      motor.turn_open()
      is_open = True

    elif command == "open5" and not is_open and enabled:
      motor.turn_open()
      is_open = True
      forced_open = True
      forced_end_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

    elif command == "close" and is_open and enabled:
      motor.turn_close()
      is_open = False

    elif command == "close5" and is_open and enabled:
      motor.turn_close()
      is_open = False
      forced_close = True
      forced_end_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

    elif command == "disable":
      enabled = False

    elif command == "enable":
      enabled = True

    elif command == "shutdown":
      subprocess.run("shutdown now", shell=True)
      #quit()

    elif command == "restart":
      subprocess.run("reboot", shell=True)
      #quit()
   
    elif command == "open_shutter":
      shutter.open_shutter()

    elif command == "close_shutter":
      shutter.close_shutter()

  if forced_open or forced_close or not enabled:
    continue   

  now = datetime.datetime.now()
  allow_open = now.hour > 12 or now.hour <= 5 or (now.hour == 5 and now.minute <= 45)
  # always allow open
  allow_open = True

  # handle case when to open the window  
  if not is_open and allow_open:
    if co2_value >= upper_threshold:
      
      print(f"co2_value ({co2_value}), upper_threshold ({upper_threshold}), allow_open: {allow_open} -> open window")
      with open(log_filename, "a") as file:
        file.write(f"{datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')} " \
          f"{co2_value} ppm ({increment:+0.0f}), brightness: {brightness:.3f}, window is {state} -> open window\n")
      
      shutter.open_shutter()
      motor.turn_open()
      is_open = True
    
  # handle cases when to close the window
  if is_open:
    if co2_value <= lower_threshold or not allow_open:

      print(f"co2_value ({co2_value}), lower_threshold ({lower_threshold}), allow_open: {allow_open} -> close window")
      with open(log_filename, "a") as file:
        file.write(f"{datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')} " \
          f"{co2_value} ppm ({increment:+0.0f}), brightness: {brightness:.3f}, window is {state} -> close window\n")
      shutter.close_shutter()
      motor.turn_close()
      is_open = False

  # open shutter at 9:45am
  if now.hour == 9 and now.minute == 45:
    shutter.open_shutter()

  # close shutter at 20:00
  if now.hour == 20 and now.minute == 0:
    shutter.close_shutter()

