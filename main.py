from stepper_class import stepper_class
from coordinates_manager import coordinates_manager
from rotaryencoder_class import rotaryencoder_class
from accel_class import accel_class
from multiprocessing import Process
import os
import sys
import math

###############################################################################

def initializeTextFile(filename):
    if not os.path.exists(filename):
        file1 = open(filename, "w+")
        file1.write(str(0.0))
        file1.close()
    return True

#write new value to text file, or read from text file
def updateTextFile(filename, override, write_value):
    error = False
    if override == True:
        try:
            file1 = open(filename, "r+")
            angle = file1.read()
            file1.seek(0)
            file1.truncate()
            file1.write(str(write_value))
            file1.close()
        except:
            error = True
    else:
        try:
            file1 = open(filename, "r")
            angle = file1.read()
            file1.close()
        except:
            error = True
    if error == False:
        return float(angle)
    else:
        return None

###############################################################################

def clearScreen():
    if os.name == 'nt': #Windows OS
        os.system('cls')
    else:
        os.system('clear')
    return True

###############################################################################

def printMainMenu():
    print("MAIN MENU")
    print("0. Select Object")
    print("1. Calibrate Telescope")
    print("2. Set Time and Location")
    print("3. Start Tracking")
    print("Q. Quit")
    return True

def MainMenu():
    printMainMenu()
    while True:
        selection = str(input("Input: "))
        if selection == 'Q':
            return -1
        try:
            n = int(selection)
            if n >= 0 and n <= 4:
                return n
        except:
            pass
        clearScreen()
        printMainMenu()
        print("ERROR: Invalid input")

###############################################################################

def printSetObjectMenu():
    print("SELECT OBJECT")
    print("Select Category:")
    print("0. Messier or NGC Object")
    print("1. Solar System Planets and Moon")
    print("2. Other")
    return True

def setObject():
    clearScreen()
    printSetObjectMenu()
    while True:
        selection = str(input("Input: "))
        if selection == 'Q':
            n = -1
            break
        try:
            n = int(selection)
            if n >= 0 and n <= 1:
                break
        except:
            pass
        clearScreen()
        printSetObjectMenu()
        print("ERROR: Invalid input")
    
    if n == -1:
        return [False, "", n]
    
    clearScreen()
    while True:
        selection = str(input("Enter object name: "))
        choice = input("The object you have selected is \'" + str(selection) + "\'. Are you sure? [Y/n]: ")
        if choice == 'Y':
            return [True, selection, n]

###############################################################################

def printCalibrateTelescopeMenu():
    print("CALIBRATE TELESCOPE")
    print("AZIMUTH:")
    print("0. Az Move Motor")
    print("1. Az Zero")
    print("2. Az Set Angle")
    print("ALTITUDE:")
    print("3. Alt Move Motor")
    print("4. Alt Zero")
    print("5. Alt Set Angle")
    print("6. Calibrate Az")
    print("7. View Current Coordinates")
    return True

def calibrateTelescope():
    clearScreen()
    printCalibrateTelescopeMenu()
    while True:
        selection = str(input("Input: "))
        if selection == 'Q':
            n = -1
            break
        try:
            n = int(selection)
            if n >= 0 and n <= 7:
                break
        except:
            pass
        clearScreen()
        printCalibrateTelescopeMenu()
        print("ERROR: Invalid input")

    if n == -1:
        return [False, -1, 0.0]
    elif n == 1 or n == 4 or n >= 6:
        return [True, n, 0.0]
    
    clearScreen()
    while True:
        selection = str(input("Enter Angle: "))
        try:
            angle = float(selection)
            choice = input("The angle you have selected is " + str(selection) + " degrees. Are you sure? [Y/n]: ")
            if choice == 'Y':
                return [True, n, angle]
        except:
            pass
        clearScreen()

###############################################################################

#Closes all ports in array a
def closeAllPorts(a):
    for i in range(0,len(a),1):
        a[i].s.closePort()
    return True

#######################################################################################
#######################################################################################

if __name__ == "__main__":
    
    #Make input function Python version-agnostic (override Python 2 input function)
    if sys.version_info[0] < 3: #if not Python 3
        try:
            input = raw_input
        except NameError:
            pass
    
    #Markham, Ontario, Canada
    lat = 43.874168
    lon = -79.258743
    utc_offset = -5
    
    #Initialize coordinates_manager object
    c = coordinates_manager()
    c.setLocation(lat, lon, 200, utc_offset)
    
    ###############################################################################
    #Stepper Motors
    
    #Stepper Motor 1 (Az)
    s1 = stepper_class(26, 19, 0, 11, [5, 6, 13])
    s1.setupGPIO()
    s1.SleepResetHigh()
    
    #Stepper Motor 2 (Alt)
    s2 = stepper_class(25, 8, 7, 1, [16, 20, 21])
    s2.setupGPIO()
    s2.SleepResetHigh()
    
    micro_step_calibration = '1/8'
    micro_step_tracking = '1/4'
    
    timing_belt_pitch = 2.0 #2mm pitch
    timing_pulley_teeth = 20.0 #20 teeth
    big_pulley_teeth = (10 * 25.4 * math.pi) / timing_belt_pitch  #25.4mm per 1in
    gear_factor = big_pulley_teeth / timing_pulley_teeth
    
    #Initialize text files that store the position of each stepper motor
    az_pos_filename = "az_pos.txt"
    alt_pos_filename = "alt_pos.txt"
    initializeTextFile(az_pos_filename)
    initializeTextFile(alt_pos_filename)
    az_pos_temp = updateTextFile(az_pos_filename, False, 0)
    alt_pos_temp = updateTextFile(alt_pos_filename, False, 0)
    if az_pos_temp != None:
        s1.setPos(az_pos_temp * gear_factor)
    if alt_pos_temp != None:
        s2.setPos(alt_pos_temp * gear_factor)
    

    ###############################################################################
    #Rotary Encoders
    
    #Note: the gear attached to the rotary encoder has the same number of teeth
    #and pitch as the the gear attached to the stepper motor.
    PPR = 1000 #1000 pulses per revolution for encoder
    port1 = '/dev/ttyUSB1'
    port2 = '/dev/ttyUSB0'
    #port1 = 'COM6'
    #port2 = 'COM6'
    
    #Rotary Encoder 1 (Az)
    e1 = rotaryencoder_class(PPR)
    e1.setup(port1, 9600) #setup encoder; baudrate is 9600
    
    #Rotary Encoder 2 (Alt)
    e2 = rotaryencoder_class(PPR)
    e2.setup(port2, 9600) #setup encoder; baudrate is 9600
    
    ###############################################################################
    #Other sensors
    
    #GY-521/MPU-6000
    port3 = '/dev/ttyUSB2'
    accel = accel_class()
    accel.setup(port3, 9600) #baudrate is 9600
    
    ###############################################################################
    
    #Main Menu
    while True:
        clearScreen()
        a = MainMenu()
        
        #Set Object
        if a == 0:
            object_return = setObject()
            if object_return[0] == True:
                c.setTarget(object_return[1], object_return[2])
                c.updateCoordinate()

        #Calibrate Telescope
        elif a == 1:
            calibrate_return = calibrateTelescope()
            if calibrate_return[0] == True:
                #0. Az Move Motor
                if calibrate_return[1] == 0:
                    s1.rotate(calibrate_return[2] * gear_factor, micro_step_calibration, 0.001)
                    e1.updateAngle()
                    az_pos_temp = e1.getAngle()
                    s1.setPos(az_pos_temp)
                    az_pos_temp /= gear_factor
                    updateTextFile(az_pos_filename, True, az_pos_temp)
                #1. Az Zero
                elif calibrate_return[1] == 1:
                    s1.setZero()
                    e1.setZero()
                    updateTextFile(az_pos_filename, True, 0.0)
                #2. Az Set Angle
                elif calibrate_return[1] == 2:
                    s1.setPos(calibrate_return[2] * gear_factor)
                    e1.setAngle(calibrate_return[2] * gear_factor)
                    updateTextFile(az_pos_filename, True, calibrate_return[2])
                #3. Alt Move Motor
                elif calibrate_return[1] == 3:
                    s2.rotate(calibrate_return[2] * gear_factor, micro_step_calibration, 0.001)
                    e2.updateAngle()
                    alt_pos_temp = e2.getAngle()
                    s2.setPos(alt_pos_temp)
                    alt_pos_temp /= gear_factor
                    updateTextFile(alt_pos_filename, True, alt_pos_temp)
                #4. Alt Zero
                elif calibrate_return[1] == 4:
                    s2.setZero()
                    e2.setZero()
                    updateTextFile(alt_pos_filename, True, 0.0)
                #5. Alt Set Angle
                elif calibrate_return[1] == 5:
                    s2.setPos(calibrate_return[2] * gear_factor)
                    e2.setAngle(calibrate_return[2] * gear_factor)
                    updateTextFile(alt_pos_filename, True, calibrate_return[2])
                #6. Calibrate Az
                elif calibrate_return[1] == 6:
                    #Minimize x value from accelerometer
                    if accel.s.s.is_open == False: #if serial port closed
                        accel.s.s.open()
                        #Get rid of the potentially messed up data
                        for i in range(0,10,1):
                            try:
                                a = accel.getAccel()
                            except:
                                a.s.closePort()
                    n = 5 #number of values to average
                    acc = []
                    avg = 0.0
                    tolerance = 200 #deviation tolerance for acceleration value (1g = 16384)
                    currentAngle = 0.0
                    newAngle= 0.0
                    while True:
                        try:
                            accel.update()
                            a = accel.getAccel()
                        except:
                            a.s.closePort()
                            break
                        acc += a[0] #take x value of acceleration
                        if len(acc) == n:
                            for i in range(0,n,1):
                                avg += acc[i]
                            avg /= n
                            if (avg >= -1 * tolerance) and (avg <= tolerance):
                                break
                            newAngle = float(-1.0) * math.acos(avg / 2**14) * gear_factor #new angle to move to
                            e2.updateAngle()
                            newAngle = e2.getAngle() + newAngle
                            s2.moveTo(newAngle, micro_step_tracking, 0.001)
                            e2.updateAngle()
                            s2.setPos = e2.getAngle()
                            acc = []
                            avg = 0.0
                    accel.s.closePort()
                    s2.setZero()
                    e2.setZero()
                    updateTextFile(alt_pos_filename, True, 0.0)
                #7. View Current Coordinates
                elif calibrate_return[1] == 7:
                    e1.updateAngle()
                    e2.updateAngle()
                    print("Az.: " + str(e1.getAngle() / gear_factor) + " degrees; Alt.: " + str(e2.getAngle() / gear_factor) + " degrees")
                    temp = input("Press any key and enter to continue: ")
        elif a == 2:
            pass #will add option later
        
        #Track
        elif a == 3:
            print("Tracking is ongoing")
            while True:
                try:
                    c.updateCoordinate()                        
                    m1 = Process(target=stepper_class.moveTo, args=(s1, c.az * gear_factor, micro_step_tracking, 0.001)) #No parentheses after moveTo
                    m2 = Process(target=stepper_class.moveTo, args=(s2, c.alt * gear_factor, micro_step_tracking, 0.001))
                    m1.start()
                    m2.start()
                    m1.join()
                    m2.join()
                    
                    #Update text files
                    e1.updateAngle()
                    az_pos_temp = e1.getAngle()
                    s1.setPos(az_pos_temp)
                    az_pos_temp /= gear_factor
                    updateTextFile(az_pos_filename, True, az_pos_temp)
                    
                    e2.updateAngle()
                    alt_pos_temp = e2.getAngle()
                    s2.setPos(alt_pos_temp)
                    alt_pos_temp /= gear_factor
                    updateTextFile(alt_pos_filename, True, alt_pos_temp)
                    
                    print("AZ: ", az_pos_temp)
                    print("ALT:", alt_pos_temp)
                except KeyboardInterrupt:
                    break
                except:
                    closeAllPorts([e1,e2,accel]) #for safety
                    print("ERROR")
                    break
        #For testing only
        elif a == 4:
            while True:
                try:
                    e1.updateAngle()
                    az_pos_temp = e1.getAngle()
                    s1.setPos(az_pos_temp)
                    az_pos_temp /= gear_factor
                    updateTextFile(az_pos_filename, True, az_pos_temp)
                    
                    e2.updateAngle()
                    alt_pos_temp = e2.getAngle()
                    s2.setPos(alt_pos_temp)
                    alt_pos_temp /= gear_factor
                    updateTextFile(alt_pos_filename, True, alt_pos_temp)
                    
                    print("AZ: ", az_pos_temp)
                    print("ALT:", alt_pos_temp)
                except KeyboardInterrupt:
                    break
                except:
                    closeAllPorts([e1,e2,accel]) #for safety
                    print("ERROR")
                    break
        #Quit
        elif a == -1:
            closeAllPorts([e1,e2,accel])
            break
