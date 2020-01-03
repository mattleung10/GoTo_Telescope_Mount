import serial

class serialComm_class:
    def __init__(self):
        self.s = serial.Serial() #serial class object
        self.portName = None
        self.baudrate = None
        self.setupDone = False
        return None

    def setup(self, portName, baudrate):
        #https://pyserial.readthedocs.io/en/latest/shortintro.html
        #Configure port
        try:
            self.s.port = portName
            self.s.baudrate = baudrate
        except:
            return False
        
        #Open the port and go through the useless stuff in the beginning
        self.s.open()
        try:
            for i in range(0,50,1):
                data = self.s.readline()
        except:
            pass
            self.s.close()
        
        #Set internal class variables
        self.portName = portName
        self.baudrate = baudrate
        self.s.timeout = 0.1
        self.setupDone = True
        return True

    #The retrieve function retrieves data from port when called
    #Returns [False, 'errorType'] if there is an error, otherwise [True, data]
    def retrieve(self):
        if self.setupDone == False: #if setup was not done properly
            return [False, 'notsetup']
        if self.s.is_open == False: #if port is closed
            return [False, 'closed']
        
        #get data
        data = None
        try:
            self.s.reset_input_buffer()
            #for safety, get rid of data that might be wrong
            for i in range(0,5,1):
                data = self.s.readline()
            data = (self.s.readline())[:-2].decode('utf-8')
        except:
            self.s.close()
            return [False, data]
        return [True, data]

    def closePort(self):
        self.s.close()
        return True
