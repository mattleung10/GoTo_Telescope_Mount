#For use with Longrunner A4988 Stepper Motor Driver Module

import RPi.GPIO as GPIO
import time
from multiprocessing import Value

class stepper_class:
    def __init__(self, direction, step, sleep, reset, ms):
        self.di = direction
        self.st = step
        self.sl = sleep
        self.re = reset
        self.ms = ms
        self.resolution = {'1/1': (0, 0, 0),
                           '1/2': (1, 0, 0),
                           '1/4': (0, 1, 0),
                           '1/8': (1, 1, 0),
                           '1/16': (1, 1, 1)}
        self.SPR = 200 #steps per revolution
        self.GPIOsetup = False #whether or not the GPIO pins have been set up
        
        #https://stackoverflow.com/a/45312180
        #https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Value
        #In order for multiprocessing to work, self.pos must be a Value object,
        #It will be a shared memory object that can be modified through the processes
        self.__pos = Value('d', 0.0) #double underscore for private variable; pos is in degrees
    
    #sets up the GPIO pins
    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.di, GPIO.OUT)
        GPIO.setup(self.st, GPIO.OUT)
        GPIO.setup(self.sl, GPIO.OUT)
        GPIO.setup(self.re, GPIO.OUT)
        for i in range(0,len(self.ms),1):
            GPIO.setup(self.ms[i], GPIO.OUT)
        self.GPIOsetup = True
        return True

    #Set SLEEP and RESET pins (both must be set to high)
    def SleepResetHigh(self):
        if self.GPIOsetup == False:
            return False
        
        GPIO.output(self.sl, GPIO.HIGH)
        GPIO.output(self.re, GPIO.HIGH)
        return True

    def setPos(self, pos):
        self.__pos.value = pos
        return True
    
    def getPos(self):
        return self.__pos.value
    
    def setZero(self):
        self.__pos.value = 0.0
        return True

###############################################################################

    #Turns motor shaft by angle degrees
    def rotate(self, angle, micro_step, delay):
        if self.GPIOsetup == False:
            return False
        
        GPIO.output(self.ms, self.resolution[micro_step]) #set up Microstep Select (MS1, MS2, MS3) logic inputs

        frac = abs(angle) / float(360) #must 360 into a float for frac to be a float
        step_count = int(self.SPR * int(micro_step[2:len(micro_step)]) * frac)
        if step_count == 0:
            return False
        
        if angle >= 0:
            GPIO.output(self.di, 1)
        else:
            GPIO.output(self.di, 0)
        incr = float(angle) / step_count
        
        for i in range(0,step_count,1):
            GPIO.output(self.st, GPIO.HIGH)
            GPIO.output(self.st, GPIO.LOW)
            self.__pos.value += incr
            time.sleep(delay)
                
        return True
        
    #Turns motor shaft to abs_angle
    def moveTo(self, abs_angle, micro_step, delay):
        if self.GPIOsetup == False:
            return False
        diff = abs_angle - self.__pos.value
        self.rotate(diff, micro_step, delay)
        return True

