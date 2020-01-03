# GoTo_Telescope_Mount

A GoTo mount is a computerized telescope mount that can automatically point a telescope at a certain astronomical object. I made my own alt-azimuth mount controlled by a Raspberry Pi and Arduinos for my 4.5" Newtonian Telescope.

### Key Features
-	Internal database of all Messier and NGC objects (scraped from the Strasbourg Astronomical Data Centre)
-	Feedback control system using optical rotary encoders
-	Axis calibration using accelerometers
-	Mount can be controlled from another device
-	Entire mount can be powered by simply plugging it into the wall

![](https://github.com/mattleung10/GoTo_Telescope_Mount/blob/master/images/GoToDemo_600.gif)

## To Use

Run the ```main.py``` program.

### Libraries Used
- astropy, for coordinate transformations and calculations
- multiprocessing, for object tracking in parallel
- pySerial, for serial communication
- pandas, to handle CSV files
- os and sys, for manipulating files, and to determine Python version and OS type
- datetime, to determine current time
