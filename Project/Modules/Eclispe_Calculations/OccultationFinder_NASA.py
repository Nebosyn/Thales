import spiceypy as sp
import math
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Constants.constants import scaleCoff
from ..Eclispe_Calculations.City_EclipseChecker import calculatePenumbraRadius
from ..Eclispe_Calculations.EclipseSimualtion import createEclipseRays
def findEclipses():
    maxwin = 20000
    maxivl = int(maxwin/2)
    window = sp.stypes.SPICEDOUBLE_CELL(maxwin)
    result = sp.stypes.SPICEDOUBLE_CELL(maxwin)
    # print("Version:" + sp.tkvrsn("Toolkit"))
    # metaKernel = getFilePath("meta-kernel.txt")
    # os.chdir(os.path.dirname(metaKernel))
    # sp.furnsh(metaKernel)
    # file = open(metaKernel,"r")
    # kernelsList = (file.read().split("(")[1]).split(")")[0]
    # print ("Loading kernels:")
    # print(kernelsList)
    # file.close
    # print("Kernels loaded!")
    start_time_utc = "1900 september 1 00:00:00"
    end_time_utc = "2140 December 1 00:00:00"
    # print("Start time: ",start_time_utc)
    # print("End time: ",end_time_utc)
    start_time = sp.str2et(start_time_utc)
    end_time = sp.str2et(end_time_utc)
    sp.wninsd(start_time,end_time,window)
    window = angualSeparationFinder(maxivl,window,result)
    eclipsesList = occultationFinder(window)
    return eclipsesList

def angualSeparationFinder(maxivl,window,result):
    observer = "EARTH"
    limitDegrees = 3
    limitRadians =  math.radians(limitDegrees)
    relate = "<"
    step = 5*sp.spd()
    adjust = 0
    # print("Starting angular separation search")
    sp.gfsep("MOON", "POINT", " ","SUN",  "POINT", " ","NONE",observer,relate,limitRadians,adjust,step,maxivl,window,result)
    # print("Done")
    window = sp.copy(result)
    # print("GFSEP FUNCTION OUTPUT window:",window)
    return window

def occultationFinder(window):
    step = 60
    eclipses = sp.gfoclt("PARTIAL","moon","ellipsoid","iau_moon","sun","ellipsoid","iau_sun","NONE","EARTH",step,window)
    i = 0
    eclipses_list = []
    while i<sp.wncard(eclipses):
        [left,right] = sp.wnfetd(eclipses , i)
        start_of_eclipse = sp.timout(left,"YYYY Mon DD HR:MN:SC ::UTC\n")
        # print(f"START: {start_of_eclipse}")
        end_of_eclipse = sp.timout(right,"YYYY Mon DD HR:MN:SC ::UTC")
        # print(f"END:   {end_of_eclipse}")
        eclipses_list.append([start_of_eclipse,end_of_eclipse])
        i+=1
    return eclipses_list


def recalculateEclipseBoundaries(eclipsewindow):
    print("Recalculating eclipse...")
    startOfEclipse = sp.str2et(eclipsewindow[0])
    endOfEclipse = sp.str2et(eclipsewindow[1])
    timeStep = [3600,1800,600,60,30,10,1]
    earthSpecs = getCelestialObjectSpecs("EARTH",endOfEclipse,scaleCoff)
    moonSpecs = getCelestialObjectSpecs("MOON",endOfEclipse,scaleCoff)
    sunSpecs = getCelestialObjectSpecs("SUN",endOfEclipse,scaleCoff)
    penumbraRadius = calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
    startOfEclipse = findEclipseBoundaries(startOfEclipse,timeStep,penumbraRadius,"-")
    endOfEclipse = findEclipseBoundaries(endOfEclipse,timeStep,penumbraRadius,"+")
    print("Done")
    return (sp.et2utc(startOfEclipse,"C",0),sp.et2utc(endOfEclipse,"C",0)), penumbraRadius

def findEclipseBoundaries(eclipseBoundary,timeStep,penumbraRadius,typeOfRecalculation):
    timeStepChooser = 0
    timeToChange = eclipseBoundary
    while timeStepChooser<=6:
        if typeOfRecalculation == "+":
            eclipseBoundary = (timeToChange + timeStep[timeStepChooser])
        elif typeOfRecalculation == "-":
            eclipseBoundary = (timeToChange - timeStep[timeStepChooser])
        earthSpecs = getCelestialObjectSpecs("EARTH",eclipseBoundary,scaleCoff)
        moonSpecs = getCelestialObjectSpecs("MOON",eclipseBoundary,scaleCoff)
        sunSpecs = getCelestialObjectSpecs("SUN",eclipseBoundary,scaleCoff)
        result = createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Instant")
        if result != None:
            timeToChange = eclipseBoundary
        elif result == None:
            timeStepChooser+=1
    return eclipseBoundary