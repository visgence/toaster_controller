#!/usr/bin/python

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

time = 0
prev_temp = setpoints[0]['temp']
prev_time = setpoints[0]['t_plus']

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
     
    prev_temp = setpoints[i]['temp']
    prev_time = setpoints[i]['t_plus']
   


