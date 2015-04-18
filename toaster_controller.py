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
import matplotlib.gridspec as gridspec
import numpy as np

from time import sleep
from matplotlib import pylab

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help="Input Profile File to Convert")
    parser.add_argument('--port', help="Input Serial Port", required = True)
    args = parser.parse_args()

    print "template file : %s " % args.profile
    print "profile file : %s " % args.port

    with open(args.profile) as f:
        setpoints = json.load(f)
    f.close()

    #init Serial Controller
    print "Init Serial"
    serial = serial.Serial(port=args.port, baudrate=9600,timeout=0.5)
    serial.write('%');
    sleep(1)
    serial.readline()
    serial.write(struct.pack("B",0))
    print "Init Serial Finished"


    low = int(0)
    max_xy = max(setpoints)
    high = max_xy['t_plus']

    time_t = 0

    prev_temp = setpoints[0]['temp']
    prev_time = setpoints[0]['t_plus']

    max_y = max(setpoints)
    print "Max Time, %d"  % (max_y['t_plus'])

    data = {}
    datalist = []
    list_temp ={}

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

    datalist = sorted([(key,value) for(key,value) in data.items()])



    plt.ion()
    
    
    gs = gridspec.GridSpec(2, 1,height_ratios=[2,1])
    fig = plt.figure()
    ax1 = fig.add_subplot(gs[0])
    ax1.set_xlim(low,high)
    ax1.set_ylim(low,high)

    tar_title = ax1.text(0.2,1.005, '', transform=ax1.transAxes)
    cur_title = ax1.text(0.45, 1.005, '', transform=ax1.transAxes)
    set_title = ax1.text(0.7,1.005, '', transform=ax1.transAxes)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(low,high)
    ax2.set_ylim(0,32)

    wm = plt.get_current_fig_manager()
    wm.window.wm_geometry("800x900+50+50")
    
    output = 1
    wait = 0

    set = 0
    counter = 0

    #time.sleep(2)
    print "Start"

    p = pid2.PID(2,0.05,0.5,int_max=640,int_min=0)
    p.setPoint(0)

    start_time = time.time()
    temp = 0
    print "Datalist Size %d" % (len(datalist))

    for k, v in datalist:
        set_time = k
        set_temp = v
        
        p.setPoint(float(set_temp))
        #read incoming temp           
        serial.write('%');
        try:
            temp = float(serial.readline().strip());
        except ValueError:
            print "Value Error"


        pid = p.update(temp)
        if(pid>32):
            output = 32
        elif(pid<0):
            output = 0
        else:
            output = int(pid)
        
        serial.write(struct.pack("B",output))
        print "Time " + str(set_time) + " Temp: " + str(temp) + " "  + "Set_temp: " + str(set_temp)  +" PWR_SET: " + str(output) + " PID: " + str(pid)

        #graph here
        ax1.scatter(set_time,set_temp)
        ax1.scatter(set_time, temp, color='red')
        ax2.scatter(set_time, output, color='green')
        tar_title.set_text("Target %i" % (set_temp))
        cur_title.set_text("Current %i" % (temp))
        set_title.set_text("Pwr Set %i" % (output))

        plt.draw()
        #sleep(0.05)


        #break while loop and keep graph up-- before end of dict
        if set_time >= max_xy:
            break

        time.sleep(1)

    #Turn off when exiting
    print "Program Finished"
    serial.write(struct.pack("B",0))
    plt.autoscale(enable=False)
    plt.show(block=True)


