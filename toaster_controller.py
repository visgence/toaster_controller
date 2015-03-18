#!/usr/bin/env python

import sys
import struct
import time
import serial
import pid2
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument('--port', help="Input Serial Port", required = True)
parser.add_argument('--profile', help="Input Profile File")
args = parser.parse_args()

print "port is : %s " % args.port
print "profile file : %s " % args.profile

if __name__ == "__main__":

    output = 1
    wait = 0
    
    set = 0

    serial = serial.Serial(port=args.port,baudrate=9600)
    
    time.sleep(2)
    print "Start"
    
    p = pid2.PID(2,0.05,0.5,int_max=640,int_min=0)
    p.setPoint(0)

    #read file
    file = open(sys.argv[1],'r')
    start_time = time.time()


    (set_time,set_temp,msg) = file.readline().rstrip().split(",")
    #serial.write(struct.pack("B",int(set_temp))    


##simulate real-time update to plot    
#    while(1):

#        p.setPoint(float(set_temp))
           
#        temp = float(serial.readline().strip());
        
#        pid = p.update(temp)
#        if(pid>32):
#            output = 32
#        elif(pid<0):
#            output = 0
#        else:
#            output = int(pid)
        
#        print "Time " + set_time + " Temp: " + str(temp) + " "  + "Set_temp: " + set_temp  +" PID: " + str(output) + " PID: " + str(pid) + " " + msg

#        serial.write(struct.pack("B",output))

#        if(int(set_time)+start_time <= time.time()):
#            (set_time,set_temp,msg) = file.readline().rstrip().split(",")

        #time.sleep(1)


#graph generated profile



