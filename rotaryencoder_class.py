from serialComm_class import serialComm_class

class rotaryencoder_class:
    def __init__(self, PPR):
        self.__angle = None #angle of the rotary encoder
        self.s = None #serialComm_class object
        self.PPR = PPR #pulses per revolution
        self.__offset = float(0)
        self.setupDone = False #whether or not setup is done
        return None
    
    def setup(self, portName, baudrate):
        self.s = serialComm_class()
        if self.s.setup(portName, baudrate) == False: #check if setup successfully done
            return False
        self.__angle = float(0)
        self.setupDone = True
        return True
    
    def setZero(self):
        if self.setupDone == False: #if setup was not done
            return False
        self.setAngle(0.0)
        return True
    
    def setAngle(self, angle):
        if self.setupDone == False:
            return False
        self.updateAngle()
        self.__offset += -1.0 * (self.__angle - angle) #NOT self.__offset = -1.0 * (self.__angle - angle)
        self.__angle = angle
        return True
    
    def updateAngle(self):
        if self.setupDone == False: #if setup was not done
            return False
        
        r = [] #array to hold result from s.retrieve
        try:
            r = self.s.retrieve()
        except:
            self.s.closePort()
            return False
        
        if len(r) != 2:
            return False
        if r[0] == False:
            return False
        
        #encoder returns 16 bit unsigned integer (in string form)
        try:
            temp = int(r[1])
        except:
            return False
        #change into signed integer
        if 2**15 < temp and temp < 2**16:
            temp = (2**16 - temp) * -1
        self.__angle = (float(360) * temp / self.PPR) + self.__offset
        return True
    
    def getAngle(self):
        return self.__angle
    
