#!/usr/bin/python
import serial
import time
import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
args = parser.parse_args()

print "profile file : %s " % args.profile

with open(args.profile) as f:
    setpoints = json.load(f)
f.close()

"""
setpoints = [{'t_plus':0
              ,'temp':20}
            ,{'t_plus':90
              ,'temp':150
              }
            ,{'t_plus':180
              ,'temp':180
              }
            ,{'t_plus':215
              ,'temp':220
              }
            ,{'t_plus':235
              ,'temp':220
              }
            ,{'t_plus':300
              ,'temp':50
              }
            ]
"""

serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

#plots in realtime
plt.ion()

v = [0,300,0,300]

print min(setpoints)
print max(setpoints)
#print setpoints[0]

plt.axis(v)
time = 0
prev_temp = setpoints[0]['temp']
prev_time = setpoints[0]['t_plus']

data = {}

for i in range(1, len(setpoints)):
    #print setpoints[i] #DEBUG
    slope = (float(setpoints[i]['temp']) - float(prev_temp)) / (float(setpoints[i]['t_plus'] - float(prev_time)))
    #print slope #DEBUG
    time = prev_time
    temp = prev_temp

        
    while time < setpoints[i]['t_plus']:
        temp += slope
        time += 1
       
        print "%d,%d" % (time, temp)
        
        plt.scatter(time,temp)
        plt.draw()
               
        #for testing purposes
        data[time]=int(temp)

        #incoming data 
        temp1 = float(serial.readline().strip());

        plt.scatter(time, temp1, color='red')

        plt.draw()
        sleep(0.05)

    prev_temp = setpoints[i]['temp']
    prev_time = setpoints[i]['t_plus']


"""
class DynamicUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 305
    min_y = 0
    max_y = 500

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        #original values static plot
        for key, value in data.iteritems():
            self.ax.plot(key, value, 'bo')
        self.lines, = self.ax.plot([],[], 'ro')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(False)
        self.ax.set_ylim(self.min_y, self.max_y)
        self.ax.set_xlim(self.min_x, self.max_x)
        #self.ax.grid()

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def __call__(self):
        import numpy as np
        import time
        self.on_launch()
        xdata = []
        ydata = []
        for key, value in data1.iteritems():
            xdata.append(key)
            ydata.append(value)
            self.on_running(xdata, ydata)
            time.sleep(1)

        return xdata, ydata

d = DynamicUpdate()
d()
"""

plt.autoscale(enable=False)
plt.show(block=True)

#generates a json? profile
#with open('curve1.json','w') as f:
#    json.dump(data1,f)
#f.close()

#create profile template
#with open('test.json','w') as f:
#  json.dump(setpoints,f)
#f.close()
