#!/usr/bin/env python

import sys
import struct
import time
import serial
import pid2
import argparse
import json
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from time import sleep
from matplotlib import pylab

parser = argparse.ArgumentParser()
parser.add_argument('--profile', help="Input Profile File to Convert")
parser.add_argument('--port', help="Input Serial Port", required = True)
args = parser.parse_args()

print "template file : %s " % args.profile
print "profile file : %s " % args.port

with open(args.profile) as f:
    setpoints = json.load(f)
f.close()

#serial = serial.Serial(port=args.port, baudrate=9600)

low = int(0)
max_xy = max(setpoints)
high = max_xy['t_plus']

time_t = 0

prev_temp = setpoints[0]['temp']
prev_time = setpoints[0]['t_plus']

max_y = max(setpoints)
print max_y['t_plus']

data = {}

#computes the profile
for i in range(1, len(setpoints)):
#for i in range(1, 2):
    #print setpoints[i] #DEBUG
    slope = (float(setpoints[i]['temp']) - float(prev_temp)) / (float(setpoints[i]['t_plus'] - float(prev_time)))
    #print slope #DEBUG
    time_t = prev_time
    temp_t = prev_temp
    
    while time_t < setpoints[i]['t_plus']:
        temp_t += slope
        time_t += 1

       #print "%d,%d" % (time_t, temp)
        data[time_t]=int(temp_t)

    prev_temp = setpoints[i]['temp']
    prev_time = setpoints[i]['t_plus']

if __name__ == "__main__":

    plt.ion()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(low,high)
    ax1.set_ylim(low,high)

    cur_title = ax1.text(.5, 1.005, '', transform=ax1.transAxes)
    tar_title = ax1.text(.3,1.005, '', transform=ax1.transAxes)

    output = 1
    wait = 0

    set = 0
    counter = 0
    serial = serial.Serial(port=args.port, baudrate=9600)

    time.sleep(2)
    print "Start"

    p = pid2.PID(2,0.05,0.5,int_max=640,int_min=0)
    p.setPoint(0)

    #read file
    #file = open(sys.argv[1],'r')
    start_time = time.time()

    set_time = data.keys()[counter]
    set_temp = int(data.values()[counter])
    #(set_time,set_temp,msg) = file.readline().rstrip().split(",")
    #serial.write(struct.pack("B",int(set_temp))  #commented previously  

    while(1):

        p.setPoint(float(set_temp))

        #read incoming temp           
        temp = float(serial.readline().strip());
        
        pid = p.update(temp)
        if(pid>32):
            output = 32
        elif(pid<0):
            output = 0
        else:
            output = int(pid)
        
    #   print "Time " + set_time + " Temp: " + str(temp) + " "  + "Set_temp: " + set_temp  +" PID: " + str(output) + " PID: " + str(pid) + " " + msg
        print "Time " + str(set_time) + " Temp: " + str(temp) + " "  + "Set_temp: " + str(set_temp)  +" PID: " + str(output) + " PID: " + str(pid)

        #graph here
        ax1.scatter(set_time,set_temp)
        ax1.scatter(set_time, temp, color='red')
        tar_title.set_text("Target %i" % (set_temp))
        cur_title.set_text("Current %i" % (temp))

        plt.draw()
        #sleep(0.05)

        serial.write(struct.pack("B",output))

        #break while loop and keep graph up-- before end of dict
        if set_time >= max_xy:
            break

        if(int(set_time)+start_time <= time.time()):
            counter+=1
            set_time = data.keys()[counter]
            set_temp = int(data.values()[counter])
            #(set_time,set_temp,msg) = file.readline().rstrip().split(",")

        time.sleep(1)


plt.autoscale(enable=False)
plt.show(block=True)

