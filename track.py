#!/usr/bin/python3

import sys,os
import cozir
import time
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.dates as mdates
import matplotlib.units as munits
import numpy as np
import datetime
import timeit

# graphics: https://github.com/vfilimonov/co2meter

# prepare matplotlib
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter

# start matplotlib interactive mode
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot([0,1], [0,0], 'r-')
plt.show()

# settings
sampling_time = 5      # [s]
N = (int)(60/sampling_time)   # length of moving average

# open sensor handle
c = cozir.Cozir('/dev/ttyUSB0')

co2_list = []
t_list = []
start_timestamp = (float)(datetime.datetime.now().timestamp())
is_colorbar_set = False
i = 0

# test maximum sampling frequency of sensor
if False:
  start = timeit.default_timer()
  for i in range(100):
    value = c.read_CO2()
  stop = timeit.default_timer()
  print("duration per measurement: {}ms".format((stop-start)*10))

# enter main loop of measurement
while True:
  i += 1
  
  # capture current ppm value of CO2 concentration
  try:
    value = c.read_CO2()
  except:
    pass
    
  # store value
  co2_list.append(value)
  #t_list.append((float)(datetime.datetime.now().timestamp()) - start_timestamp)
  t_list.append(datetime.datetime.now())
  
  print('{} CO2: {} ppm'.format(datetime.datetime.now(), value))
  
  #line1.set_xdata(t_list)
  #line1.set_ydata(co2_list)
  
  # air quality: Outdoor air contains approximately 400 ppm; breathing generates CO2, so the indoor CO2 concentration will always be at least 400 ppm and usually higher. An indoor CO2 level of 1 150 ppm provides adequate air quality, 1 400 ppm will ensure good indoor air quality in most situations, and 1 600 ppm indicates poor air quality (CEN, 2019; Active house Alliance, 2020).
  # 400 ppm - outdoor
  # 1150 ppm - adequate
  # 1400 ppm - good
  # 1600 ppm - poor
  
  ax.clear()
  if i < 120:
    ax.plot(t_list, co2_list, color="grey", marker=".", linestyle="None")
  
  # plot moving average
  if len(co2_list) > N:
    co2_list_moving_average = np.convolve(co2_list, np.ones(N)/N, mode='valid')
    inxval = mdates.date2num(t_list[N-1:])
    points = np.array([inxval, co2_list_moving_average]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    cmap = ListedColormap(['darkgreen', 'g', 'y', 'r'])
    outdoor_concentration = 700
    norm = BoundaryNorm([outdoor_concentration+0, outdoor_concentration+400, outdoor_concentration+600, outdoor_concentration+1000, 10000], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(co2_list_moving_average)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    
    if not is_colorbar_set:
      fig.colorbar(line, ax=ax)
      plt.figtext(0.2, 0.92, "$CO_2$ Konzentration", ha="left")
      plt.figtext(0.95, 0.92, "Raumluftqualität gemäß DIN EN 13779", weight="bold", ha="right")
      plt.figtext(0.83, 0.2, "hoch", color="darkgreen", weight="bold")
      plt.figtext(0.83, 0.4, "mittel", color="g", weight="bold")
      plt.figtext(0.83, 0.6, "mäßig", color="y", weight="bold")
      plt.figtext(0.83, 0.8, "niedrig", color="r", weight="bold")
      is_colorbar_set = True

    #ax.plot(t_list[N-1:], co2_list_moving_average, "r-")
  #ax.set_xlabel("time")
  ax.set_xlim(t_list[0],t_list[-1]);
  #ax.set_title("$CO_2$ concentration")
  ax.xaxis_date()
  ax.autoscale_view()
  ax.set_ylabel("$CO_2$ [ppm], 10.000 ppm = 1 %")
  ax.grid(which="both")
  
  # save once per hour
  if i % (12*60) == 0:
    filename = "saved/{}.png".format(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d_%H-%M-%S"))
    print("save to {}".format(filename))
    plt.savefig(filename)
  
  fig.canvas.draw()
  fig.canvas.flush_events()
  
  if i < 20:
    time.sleep(.2)
  elif i < 120:
    time.sleep(1)
  else:
    time.sleep(sampling_time)
