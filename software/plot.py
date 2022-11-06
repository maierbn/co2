#!/usr/bin/python3

import sys,os
import time
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.dates as mdates
import matplotlib.units as munits
import matplotlib.patches as patches
import numpy as np
import datetime
import timeit
import argparse


# prepare matplotlib
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter
plt.rcParams.update({'font.size': 22})


# read values
log_filename = "/home/pi/co2/software/values.csv"
long_log_filename = "/home/pi/co2/software/values_with_window.csv"

# start matplotlib interactive mode
fig = plt.figure(figsize=(20,8))
ax = fig.add_subplot(111)

# read values
data = np.genfromtxt(long_log_filename, delimiter=";", converters={3: lambda s: 1.0 if "open" in str(s) else 0.0})
t_list = [datetime.datetime.fromtimestamp(d) for d in data[:,0]]
#t_list = mdates.date2num(t_list)
#t_list = data[:,0]
co2_list = data[:,1]
brightness_list = data[:,2]
open_list = [d == 1.0 for d in data[:,3]]

start_timestamp = datetime.datetime.now()-datetime.timedelta(hours=24)
if len(sys.argv) > 1:
    start_timestamp = datetime.datetime.now()-datetime.timedelta(hours=24*int(sys.argv[1]))
    print(f"start_timestamp {start_timestamp}")
end_timestamp = start_timestamp + datetime.timedelta(hours=24)
is_colorbar_set = False
  
# air quality: Outdoor air contains approximately 400 ppm; breathing generates CO2, so the indoor CO2 concentration will always be at least 400 ppm 
# and usually higher. An indoor CO2 level of 1 150 ppm provides adequate air quality, 1 400 ppm will ensure good indoor air quality in most situations, 
# and 1 600 ppm indicates poor air quality (CEN, 2019; Active house Alliance, 2020).
# 400 ppm - outdoor
# 1150 ppm - adequate
# 1400 ppm - good
# 1600 ppm - poor

ax.plot([t_list[0],t_list[-1]], [co2_list[0], co2_list[-1]], color="grey", marker=".", linestyle="None")
  
N = 10

# plot moving average
if len(co2_list) > N:
  co2_list_moving_average = np.convolve(co2_list, np.ones(N)/N, mode='valid')
  
  inxval = mdates.date2num(t_list[N-1:])
  #inxval = mdates.epoch2num(t_list[N-1:])
  
  if True:
    points = np.array([inxval, co2_list_moving_average]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    cmap = ListedColormap(['darkgreen', 'g', 'y', 'r'])
    outdoor_concentration = 700
    norm = BoundaryNorm([outdoor_concentration+0, outdoor_concentration+400, outdoor_concentration+600, outdoor_concentration+1000, 10000], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(co2_list_moving_average)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    fig.colorbar(line, ax=ax)
    plt.figtext(0.02, 0.92, f"$CO_2$ Konzentration, Datum des Plots: {datetime.datetime.now():%d.%m.%Y %H:%M:%S}", ha="left")
    plt.figtext(0.95, 0.92, "Raumluftqualität gemäß DIN EN 13779", weight="bold", ha="right")
    plt.figtext(0.83, 0.2, "hoch", color="darkgreen", weight="bold")
    plt.figtext(0.83, 0.4, "mittel", color="g", weight="bold")
    plt.figtext(0.83, 0.6, "mäßig", color="y", weight="bold")
    plt.figtext(0.83, 0.8, "niedrig", color="r", weight="bold")

  # open boxes
  previous_open = False
  open_begin_t = t_list[0]
  for t,open in zip(t_list, open_list):
    if open != previous_open:
      if open:
        open_begin_t = t
      else:
        
        rect = patches.Rectangle((open_begin_t, min(co2_list)), t-open_begin_t, max(co2_list)-min(co2_list), linewidth=1, edgecolor='y', facecolor='y', alpha=0.2)
        ax.add_patch(rect)

    previous_open = open


  #ax.set_xlabel("time")
  ax.set_xlim(mdates.date2num(start_timestamp),mdates.date2num(end_timestamp))
  #ax.set_xlim(t_list[0],t_list[-1])
  #ax.set_title("$CO_2$ concentration")
  ax.xaxis_date()
  
  
  ax.autoscale_view()
  ax.set_ylabel("$CO_2$ [ppm], 10.000 ppm = 1 %")
  ax.grid(which="both")
  
  filename = "/home/pi/co2/software/output/plot_{}.png".format(datetime.datetime.strftime(end_timestamp,"%Y-%m-%d_%H-%M-%S"))
  print("save to {}".format(filename))
  plt.savefig(filename)

  if len(sys.argv) == 1:
    plt.savefig("/home/pi/co2/software/output/current.png")

  
