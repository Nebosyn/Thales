import spiceypy as sp
from ..Constants.constants import scaleCoff
from ..Eclispe_Calculations import City_EclipseChecker
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Eclispe_Calculations.EclipseSimualtion import createEclipseRays

def findEclipses():
    start_time_utc = "1900 september 1 00:00:00"
    end_time_utc = "2140 December 1 00:00:00"
    start_time = sp.str2et(start_time_utc)
    end_time = sp.str2et(end_time_utc)
    list_of_eclipses = []
    while start_time<=end_time:
        eclipseData = recalculateEclipseBoundaries(start_time)
        list_of_eclipses.append(eclipseData)
        start_time = sp.str2et(eclipseData[0][1])
    return list_of_eclipses

def recalculateEclipseBoundaries(window_start_time):
    print("Searching for eclipses...")
    timeStep = [5400,3600,1800,600,60,30,10,1]
    start_time, penumbraRadius = findEclipseBoundaries(window_start_time,timeStep,"Default")
    print(sp.et2utc(start_time,"C",0))
    end_time, penumbraRadius = findEclipseBoundaries(start_time,timeStep,"Inverted")
    print(sp.et2utc(end_time,"C",0))
    print("Done")
    return ((sp.et2utc(start_time,"C",0), sp.et2utc(end_time,"C",0)), penumbraRadius)

def findEclipseBoundaries(startTime,timeStep,searchType):
    timeStepChooser = 0
    timeToChange = startTime
    while timeStepChooser<=7:
        startTime = (timeToChange + timeStep[timeStepChooser])
        earthSpecs = getCelestialObjectSpecs("EARTH",startTime,scaleCoff)
        moonSpecs = getCelestialObjectSpecs("MOON",startTime,scaleCoff)
        sunSpecs = getCelestialObjectSpecs("SUN",startTime,scaleCoff)
        try:
            penumbraRadius = City_EclipseChecker.calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
        except:
            penumbraRadius = 3600
        result = createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Instant")
        if searchType == "Default":  
            if result == None:
                timeToChange = startTime
            elif result != None:
                timeStepChooser+=1
        elif searchType == "Inverted":
            if result != None:
                timeToChange = startTime
            elif result == None:
                timeStepChooser+=1
    eclipseBoundary = startTime
    return eclipseBoundary, penumbraRadius

