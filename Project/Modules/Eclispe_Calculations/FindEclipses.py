import spiceypy as sp
from ..Constants.constants import scaleCoff
from ..Eclispe_Calculations import City_EclipseChecker
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Eclispe_Calculations.EclipseSimualtion import createEclipseRays
from ..Tools.tools import loading_bar
import math, time

def findEclipses():
    start_time_utc = "1901 January 1 00:00:00"
    end_time_utc = "2150 January 1 00:00:00"
    start_time = sp.str2et(start_time_utc)
    end_time = sp.str2et(end_time_utc)
    list_of_eclipses = []
    while start_time<=end_time:
        eclipseData = findEclipseBoundaries(start_time)
        list_of_eclipses.append(eclipseData)
        start_time = sp.str2et(eclipseData[1])
        loading_bar(abs(sp.str2et(start_time_utc)-start_time), end_time-sp.str2et(start_time_utc), 100)
    return list_of_eclipses

def findEclipseBoundaries(window_start_time):
    print("Searching for eclipses...")
    timeStep = [5600,3600,1800,600,60,30,10,1]
    start_time = recalculateEclipseBoundaries(window_start_time,timeStep,"Default")
    print(sp.et2utc(start_time,"C",0))
    end_time = recalculateEclipseBoundaries(start_time,timeStep,"Inverted")
    print(sp.et2utc(end_time,"C",0))
    print("Done")
    return ((sp.et2utc(start_time,"C",0), sp.et2utc(end_time,"C",0)))

def recalculateEclipseBoundaries(startTime,timeStep,searchType):
    timeStepChooser = 0
    timeToChange = startTime
    while timeStepChooser<=7:
        startTime = (timeToChange + timeStep[timeStepChooser])
        earthSpecs = getCelestialObjectSpecs("EARTH",startTime,scaleCoff)
        moonSpecs = getCelestialObjectSpecs("MOON",startTime,scaleCoff)
        sunSpecs = getCelestialObjectSpecs("SUN",startTime,scaleCoff)
        penumbraRadius = 3600/scaleCoff
        result = createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Instant",360)
        if searchType == "Default":
            if result == None:
                timeToChange = startTime
            elif result != None:
                if lunarEclipseCheck(moonSpecs[0],earthSpecs[0]) == True: 
                    timeToChange = startTime
                    continue
                timeStepChooser+=1
        elif searchType == "Inverted":
            if result != None:
                timeToChange = startTime
            elif result == None:
                timeStepChooser+=1
    eclipseBoundary = startTime
    return eclipseBoundary

def lunarEclipseCheck(moonPos,earthPos):
    xM, yM, zM = moonPos
    xE, yE, zE = earthPos
    moonVector = math.sqrt(xM**2+yM**2+zM**2)
    earthVector = math.sqrt(xE**2+yE**2+zE**2)
    print(earthVector-moonVector)
    if earthVector-moonVector < 0:
        return True
    else:
        return False
