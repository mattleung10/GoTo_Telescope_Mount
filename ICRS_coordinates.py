import pandas as pd
import math

class ICRS_coordinates():
    def __init__(self):
        self.obj = None #object
        self.objNum = None #object number (e.g. M31 ==> objNum = 31)
        self.objSource = None #M or NGC
        self.filename = None #filename of csv file storing coordinates
        self.df = None #DataFrame
        self.ra = None #right ascension
        self.dec = None #declination
    
    def setObject(self, name):
        if type(name) != str:
            return False
        
        if len(name) < 2: #check if name is valid
            return False
        
        self.obj = name
        
        if self.obj[0] == 'M' or self.obj[0] == 'm': #Messier object
            self.objNum = int(self.obj[1:len(self.obj)])
            if self.objNum > 110 or self.objNum <= 0: #check if objNum is not between 1 and 110
                self.objNum = None #invalid Messier object
                return False
            self.filename = "data/messier.csv"
            self.objSource = "M"
        elif self.obj[0:2] == "NGC" or self.obj[0:2] == "ngc": #New General Catalogue Object
            self.objNum = int(self.obj[2:len(self.obj)])
            thousands = int(math.floor(self.objNum / 1000)) #get thousands digit
            self.filename = "data/ngc" + str(thousands) + ".csv" #get correct filename for NGC data (depending on what objNum is)
            self.objSource = "NGC"
        else:
            return False

        #https://realpython.com/python-csv/#reading-csv-files-with-pandas
        #open csv file and put into Pandas DataFrame
        try:
            self.df = pd.read_csv(self.filename)
        except:
            return False
         
        if self.objSource == "M":
            index = self.objNum - 1
        elif self.objSource == "NGC":
            index = self.objNum - thousands - 1

        self.ra = float(self.df.loc[index]['RA (degrees)']) #set coordinates
        self.dec = float(self.df.loc[index]['DEC (degrees)'])
        return True
    
    def getICRSCoord(self):
        return [self.ra, self.dec]

        