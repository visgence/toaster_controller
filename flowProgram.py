#!/usr/bin/python
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

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
#

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

#fig = plt.figure()
#ax1 = fig.add_subplot(111)

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
        data[time]=int(temp)
        plt.plot(time,temp, 'bo')


    prev_temp = setpoints[i]['temp']
    prev_time = setpoints[i]['t_plus']


plt.show()
#generates a json? profile
with open('curve.json','w') as f:
    json.dump(data,f)
f.close()

#create profile template
#with open('test.json','w') as f:
#  json.dump(setpoints,f)
#f.close()
