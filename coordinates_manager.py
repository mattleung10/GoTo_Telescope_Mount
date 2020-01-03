#https://keflavich-astropy.readthedocs.io/en/latest/coordinates/observing-example.html
#https://docs.astropy.org/en/stable/coordinates/

import astropy as ast
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_body, ICRS
import datetime
from ICRS_coordinates import ICRS_coordinates

class coordinates_manager():
    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.height = 0.0
        self.utcoffset = 0.0
        self.loc = None
        self.target = None
        self.az = 0.0
        self.alt = 0.0
        
    def setLocation(self, lat, lon, height, utc_offset):
        self.lat = lat
        self.lon = lon
        self.height = height
        self.utcoffset = utc_offset * ast.units.hour
        self.loc = EarthLocation(lat=lat, lon=lon, height=200)
        ast.utils.iers.conf.auto_download = False
        return True
    
    def setTarget(self, s, target_type):
        if target_type == 0: #NGC or Messier Object
            a = ICRS_coordinates()
            if a.setObject(s) == True:
                objCoor = a.getICRSCoord()
                self.target = SkyCoord(frame=ICRS,ra=objCoor[0]*ast.units.deg, dec=objCoor[1]*ast.units.deg)
            else:
                return False
        elif target_type == 1: #solar system object
            self.target = get_body(s, time=ast.time.Time(datetime.datetime.now())-self.utcoffset) #Remember to take into account UTC offset!
        elif target_type == 2: #other
            self.target = SkyCoord.from_name(s)
        return True
    
    def getCoordinate(self):
        ctime = datetime.datetime.now() #current time (according to this computer)
        
        #https://docs.astropy.org/en/stable/api/astropy.time.Time.html#astropy.time.Time
        #Convert to astropy Time object
        t = ast.time.Time(ctime)
        #Account for offset to UTC
        t -= self.utcoffset
        
        #https://docs.astropy.org/en/stable/coordinates/transforming.html
        #https://docs.astropy.org/en/stable/api/astropy.coordinates.AltAz.html
        #Transform target to a SkyCoord object with Altitude/Azimuth coordinate system
        target_altaz = self.target.transform_to(AltAz(obstime=t,location=self.loc))  

        #https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord.to_string
        return target_altaz.to_string('decimal')

    def updateCoordinate(self):
        s = self.getCoordinate()
        space_pos = 0
        for i in range(0,len(s),1):
            if s[i] == " ":
                space_pos = i
                break
        az_new = float(s[0:space_pos])
        alt_new = float(s[space_pos+1:len(s)])
        
        self.az = az_new
        self.alt = alt_new
        return True

