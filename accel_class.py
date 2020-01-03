from serialComm_class import serialComm_class

class accel_class:
    def __init__(self):
        self.__ax = None #accel x (16 bit signed int)
        self.__ay = None #accel y (16 bit signed int)
        self.__az = None #accel z (16 bit signed int)
        self.s = None #serialComm_class object
        self.setupDone = False #whether or not setup is done
        return None
    
    def setup(self, portName, baudrate):
        self.s = serialComm_class()
        if self.s.setup(portName, baudrate) == False: #check if setup successfully done
            return False
        self.__ax = 0
        self.__ay = 0
        self.__az = 0
        self.setupDone = True
        return True
    
    def update(self):
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
        #Note: GY-521 returns accel values that are 16 bit signed integers (in string form)
        #full scale range +/- 2g (reading of 1g = 2^(16-2) = 16384)
        #Sample reading: "aX=-412 aY=-564 aZ=15920"
        result = r[1]
        #extract values
        idx = 0
        acc = ""
        xyz = 0
        while idx < len(result):
            if result[idx] == '=':
                idx += 1
                xyz += 1
                while idx < len(result):
                    if result[idx] == ' ':
                        break
                    elif self.__isNum(result[idx]) == True:
                        acc += result[idx]
                    idx += 1
                if xyz == 1:
                    self.__ax = int(acc)
                elif xyz == 2:
                    self.__ay = int(acc)
                elif xyz == 3:
                    self.__az = int(acc)
            acc = ""
            idx += 1
            
        return True
    
    #checks if character is a digit or negative sign (0,1,2,3,4,5,6,7,8,9,-), using ASCII codes
    def __isNum(self, s):
        if (ord(s) >= 48 and ord(s) <= 57) or (ord(s) == 45):
            return True
        else:
            return False
    
    def getAccel(self):
        return [self.__ax, self.__ay, self.__az]
    