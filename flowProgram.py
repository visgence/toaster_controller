#!/usr/bin/python
import serial
import time
import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

from time import sleep
from matplotlib import pylab
#
# README
# 
# This program generates a temperature profile based
# on set points and times between them. It's output is 
# a CSV file which can be fed into controller.py to 
# controll the reflow toaster
#

#
#the example profile is based on Kester EP256

parser = argparse.ArgumentParser()
parser.add_argument('--profile', help="Input Profile File")
parser.add_argument('--port', help="Input Serial Port", required = True)
args = parser.parse_args()

print "profile file : %s " % args.profile
print "designated port : %s " % args.port

with open(args.profile) as f:
    setpoints = json.load(f)
f.close()


serial = serial.Serial(port=args.port, baudrate=9600)

#plots in realtime
plt.ion()
#v = [0,300,0,300]
#plt.axis(v)

fig = plt.figure()
ax1 = fig.add_subplot(111)

low = int(0)
max_xy = max(setpoints)
#print max_y['t_plus']
high = max_xy['t_plus']
#set limits based on file?  conjured file?
ax1.set_xlim(low,high)
ax1.set_ylim(low,high)

cur_title = ax1.text(.5, 1.005, '', transform=ax1.transAxes)
tar_title = ax1.text(.3,1.005, '', transform=ax1.transAxes)

time = 0
prev_temp = setpoints[0]['temp']
prev_time = setpoints[0]['t_plus']

max_y = max(setpoints)
print max_y['t_plus']

data = {}

#for i in range(1, len(setpoints)):
for i in range(1, 2):

    #print setpoints[i] #DEBUG
    slope = (float(setpoints[i]['temp']) - float(prev_temp)) / (float(setpoints[i]['t_plus'] - float(prev_time)))
    #print slope #DEBUG
    time = prev_time
    temp = prev_temp
    
    while time < setpoints[i]['t_plus']:
        temp += slope
        time += 1
       
        print "%d,%d" % (time, temp)
       
        data[time]=temp

        ax1.scatter(time,temp)
        #incoming data 
        temp1 = float(serial.readline().strip());
        ax1.scatter(time, temp1, color='red')
        tar_title.set_text("Target %i" % (temp))
        cur_title.set_text("Current %i" % (temp1))

        plt.draw()
        #sleep(0.05)

    prev_temp = setpoints[i]['temp']
    prev_time = setpoints[i]['t_plus']
    
#for key, value in data.items():
#    print key, int(value)
#print data.items()[0]

print data.keys()[0]
print data.values()[0]


plt.autoscale(enable=False)
plt.show(block=True)

#saves until program is done, need before program is completed.
with open('curve.csv', 'a+') as f:
    writer = csv.writer(f, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key, value in data.items():
        writer.writerow([key,value])

f.close()

