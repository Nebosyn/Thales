import spiceypy as sp
import os
import time
import math
import sys
from ..Constants.constants import scaleCoff
from ..Eclispe_Calculations import City_EclipseChecker
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Celestial_Calculations.CelestialMath import pointLocationOnACelestialObject,getPointLatitundal
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

def getFilePath(fileName):
    rootDirectory = os.getcwd()
    for relativePath,dirs,files in os.walk(rootDirectory):
        if(fileName in files):
            filePath = os.path.join(rootDirectory ,relativePath,fileName)
            return(filePath)
    print("Error occured:")
    sys.exit("File " + fileName + " not found")


def recalculateEclipse(eclipsewindow):
    print("Recalculating eclipse...")
    startOfEclipse = sp.str2et(eclipsewindow[0])
    endOfEclipse = sp.str2et(eclipsewindow[1])
    timeStep = [3600,1800,600,60,30,10,1]
    timeStepChooser = 0
    timeToChange = startOfEclipse
    earthSpecs = getCelestialObjectSpecs("EARTH",endOfEclipse,scaleCoff)
    moonSpecs = getCelestialObjectSpecs("MOON",endOfEclipse,scaleCoff)
    sunSpecs = getCelestialObjectSpecs("SUN",endOfEclipse,scaleCoff)
    penumbraRadius = City_EclipseChecker.calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
    startOfEclipse = eclipseRecalculationCycle(startOfEclipse,timeStep,penumbraRadius,"-")
    endOfEclipse = eclipseRecalculationCycle(endOfEclipse,timeStep,penumbraRadius,"+")
    print("Done")
    return (sp.et2utc(startOfEclipse,"C",0),sp.et2utc(endOfEclipse,"C",0)), penumbraRadius

def eclipseRecalculationCycle(eclipseBoundary,timeStep,penumbraRadius,typeOfRecalculation):
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

def createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,typeOfCreation):
    function_start_time = time.time()
    earthPos = earthSpecs[0]
    earthRadius = earthSpecs[1]/2
    moonPos = moonSpecs[0]
    moonRadius = moonSpecs[1]/2
    sunPos = sunSpecs[0]
    sunRadius = sunSpecs[1]/2
    earthX = earthPos[0]
    earthY = earthPos[1]
    earthZ = earthPos[2]
    moonX = moonPos[0]
    moonY = moonPos[1]
    moonZ = moonPos[2]
    sunX = sunPos[0]
    sunY = sunPos[1]
    sunZ = sunPos[2]
    sun_moonDistance = math.sqrt((moonX-sunX)**2+(moonY-sunY)**2+(moonZ-sunZ)**2)
    numberOfRays = 360
    anglesBetweenSunAndMoon = getPointLatitundal(sunPos,moonPos)
    xangleSunMoon = anglesBetweenSunAndMoon[0]
    yangleSunMoon = anglesBetweenSunAndMoon[1]
    zangleSunMoon = anglesBetweenSunAndMoon[2]
    rayOffset = (2*math.pi)/numberOfRays
    listOfIntersections = []
    for ray in range(numberOfRays):
        ray+=1
        startOfRayPos = pointLocationOnACelestialObject(sunPos,penumbraRadius,rayOffset*ray,zangleSunMoon+math.radians(90))
        # createCamera(startOfRayPos,(0,0,0),f"STARTOFRAYPOS{ray}",1)
        endOfRayPos = pointLocationOnACelestialObject(moonPos,penumbraRadius,rayOffset*ray,zangleSunMoon+math.radians(90))
        # createCamera(endOfRayPos,(0,0,0),f"ENDOFRAYPOS{ray}",1)
        # print(f" index: {ray}  numberOfPoints: {numberOfRays}")
        # print("")
        # print("")
        pointOfIntersection = City_EclipseChecker.calculateRayIntersection(startOfRayPos,endOfRayPos,earthPos,earthRadius,1)
        # print(endOfRayPos)
        if pointOfIntersection == None:
            continue
        if typeOfCreation.lower() == "instant":
            return pointOfIntersection
        listOfIntersections.append(pointOfIntersection)
    if typeOfCreation.lower() == "full":
        # print(f"TIME:           {time.time() - function_start_time}")
        return listOfIntersections
    return None

def fullRayCast(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,typeOfCreation):
    pointsList = []
    radiusDecrease = 100/scaleCoff
    while penumbraRadius>0:
        pointsList.append(createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,typeOfCreation))
        penumbraRadius -= radiusDecrease
    return pointsList,radiusDecrease

def createEclipseShadowMapping(earthSpecs,moonSpecs,sunSpecs,penumbraRadius):
        solarEclipseCenterPos = City_EclipseChecker.calculateRayIntersection(sunSpecs[0],moonSpecs[0],earthSpecs[0],earthSpecs[1]/2,1)
        if solarEclipseCenterPos != None:
            penumbraRadius = City_EclipseChecker.calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
        listOfIntersections,radiusDecrease = fullRayCast(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Full")
        return listOfIntersections, radiusDecrease