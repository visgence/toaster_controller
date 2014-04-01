#-------------------------------------------------------------------------------
# PID.py
# A simple implementation of a PID controller
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
# Integral Max and Min Added by Evan Salazar (evan@visgence.com)
#-------------------------------------------------------------------------------

import time

class PID:
    """ Simple PID control.

        This class implements a simplistic PID control algorithm. When first
        instantiated all the gain variables are set to zero, so calling
        the method GenOut will just return zero.
    """
    def __init__(self,Kp=0,Ki=0,Kd=0,int_max=500,int_min=-500):
        # initialze gains
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.int_max = int_max
        self.int_min = int_min

        self.Initialize()

    def setPoint(self,set_point):
        self.set_point = set_point    

    def SetKp(self, invar):
        """ Set proportional gain. """
        self.Kp = invar

    def SetKi(self, invar):
        """ Set integral gain. """
        self.Ki = invar

    def SetKd(self, invar):
        """ Set derivative gain. """
        self.Kd = invar

    def SetPrevErr(self, preverr):
        """ Set previous error value. """
        self.prev_err = preverr

    def Initialize(self):
        # initialize delta t variables
        self.currtm = time.time()
        self.prevtm = self.currtm

        self.prev_err = 0

        # term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0


    def GenOut(self, error):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the error signal from a summing junction
            (the error parameter).
        """
        self.currtm = time.time()               # get t
        dt = self.currtm - self.prevtm          # get delta t
        de = error - self.prev_err              # get delta error

        self.Cp = self.Kp * error               # proportional term
        self.Ci += error * dt                   # integral term

        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de/dt                     # derivative term

        if self.Ci > self.int_max:
            self.Ci = self.int_max
        
        elif self.Ci < self.int_min:
            self.Ci = self.int_min


        self.prevtm = self.currtm               # save t for next pass
        self.prev_err = error                   # save t-1 error

        # sum the terms and return the result
        #print "P: %f I: %f D %f" % (self.Cp,(self.Ki * self.Ci),(self.Kd * self.Cd))
        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)
    
    def update(self,value):
        return  self.GenOut(self.set_point-value)
