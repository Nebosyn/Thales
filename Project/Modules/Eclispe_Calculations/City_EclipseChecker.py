import math
import csv
import spiceypy as sp
import os,sys
from ..Constants.constants import scaleCoff
from ..Tools.tools import getFilePath
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Celestial_Calculations.CelestialMath import pointLocationOnACelestialObject,getPointLatitundal

def CityEclipseCheck(window:tuple,scaleCoff:int,programMode:int,penumbraRadius:any,chosenCountries):
    print("Executing cities scan...")
    currentDirectory = os.path.dirname(os.getcwd())
    os.chdir(currentDirectory)
    with open("worldcities.csv","r",encoding="UTF-8") as f:
        startOfEclipse = sp.utc2et(window[0])
        endOfEclipse = sp.utc2et(window[1])
        step = 60
        unfilteredCitiesData = list(csv.reader(f))
        citiesData = []
        for cityData in unfilteredCitiesData:
            if programMode == 1 and cityData[8] == "primary":
                citiesData.append(cityData)
            if programMode == 2 and (cityData[8] == "primary" or cityData[8] == "admin"):
                citiesData.append(cityData)
            if programMode == 3 and cityData[4] in chosenCountries:
                citiesData.append(cityData)
        eclipsedCities = []
        currentTime = startOfEclipse
        while currentTime<=endOfEclipse:
            earthSpecs = getCelestialObjectSpecs("EARTH",currentTime,scaleCoff)
            moonSpecs = getCelestialObjectSpecs("MOON",currentTime,scaleCoff)
            sunSpecs = getCelestialObjectSpecs("SUN",currentTime,scaleCoff)
            # print(f"Ephemeris: {currentTime}; ")
            for cityData in citiesData:
                eclipsedCity = cityEclipseCheck(cityData,earthSpecs,moonSpecs,sunSpecs,penumbraRadius,currentTime)
                if eclipsedCity != None:
                    eclipsedCities.append(eclipsedCity)
                    citiesData.remove(cityData)
            currentTime = currentTime+step
        print("Done\n")
        return eclipsedCities

def cityEclipseCheck(cityData,earthSpecs,moonSpecs,sunSpecs,penumbraRadius,time):
        eclipsedCities = {}
        cityName,cityLatitundal,cityCountry = cityData[1],(float(cityData[2]),float(cityData[3])),cityData[4]
        # print(f"City Name: {cityName}")
        cityRectangular = getCityLocation(cityLatitundal,earthSpecs[0],earthSpecs[1]/2,time)
        if calculateRayIntersection(sunSpecs[0],cityRectangular,earthSpecs[0],earthSpecs[1]/2,2) == None:
            return None
        if calculateRayIntersection(sunSpecs[0],cityRectangular,moonSpecs[0],penumbraRadius,1)!= None:
            # print(f"Appended City: {cityName}")
            if cityCountry not in eclipsedCities.keys():
                eclipsedCities[cityCountry] = []
            return cityName,cityLatitundal
        else:
            return None

def checkEclipseVisibility(penumbraRadius,solarEclipseCenterPos,pointPos,pointOfIntersection,radiusOfSphere):
    pointPosX = pointPos[0]
    pointPosY = pointPos[1]
    pointPosZ = pointPos[2]
    if solarEclipseCenterPos != None:
        print(f"solarEclipseCenterPos{solarEclipseCenterPos}      pointPos{pointPos}")
        solarEclipseX = solarEclipseCenterPos[0]
        solarEclipseY = solarEclipseCenterPos[1]
        solarEclipseZ = solarEclipseCenterPos[2]
        result = ((pointPosX-solarEclipseX)**2+(pointPosY-solarEclipseY)**2+(pointPosZ-solarEclipseZ)**2)
        # print(f"result {result}")
        # print(f"Radius {penumbraRadius**2}")
        if result <= penumbraRadius**2:
            return 1
        else:
            return 0
    else:
        pointOfIntersectionX = pointOfIntersection[0]
        pointOfIntersectionY = pointOfIntersection[1]
        pointOfIntersectionZ = pointOfIntersection[2]
        result = ((pointPosX-pointOfIntersectionX)**2+(pointPosY-pointOfIntersectionY)**2+(pointPosZ-pointOfIntersectionZ)**2)
        if result <= radiusOfSphere**2:
            return 1
        else:
            return 0 

def getAvailableCountries():
    availableCountries = []
    try:
        filePath = getFilePath("worldcities.csv")
        with open(filePath,'r',encoding="UTF-8") as file:
            citiesData = list(csv.reader(file))
            for cityData in citiesData:
                cityCountry = cityData[4]
                if cityCountry not in availableCountries:
                    availableCountries.append(cityCountry)
            return availableCountries
    except:
        sys.exit("File worldcities.csv not found.")
    
def calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs):
    earthPos = earthSpecs[0]
    moonPos = moonSpecs[0]
    sunPos = sunSpecs[0]
    earthX = earthPos[0]
    earthY = earthPos[1]
    earthZ = earthPos[2]
    moonX = moonPos[0]
    moonY = moonPos[1]
    moonZ = moonPos[2]
    sunX = sunPos[0]
    sunY = sunPos[1]
    sunZ = sunPos[2]
    earthRadius = earthSpecs[1]/2
    moonRadius = moonSpecs[1]/2
    sunRadius = sunSpecs[1]/2
    earth_sunDistance = math.sqrt((earthX-sunX)**2+(earthY-sunY)**2+(earthZ-sunZ)**2)
    # print(earth_sunDistance)
    moon_earthDistance = math.sqrt(((moonX-earthX)**2+(moonY-earthY)**2+(moonZ-earthZ)**2))
    # print(moon_earthDistance)
    penumbraRadius = moonRadius*(1+((sunRadius/earth_sunDistance)/(moonRadius/moon_earthDistance)))
    # umbraRadius = moonRadius - ((moon_earthDistance-earthRadius)/(earth_sunDistance-moon_earthDistance))*(sunRadius-moonRadius)
    # print(umbra)
    return penumbraRadius

def calculateRayIntersection(startOfRayPos:tuple,endOfRayPos,centerOfSphericalObject:tuple,sphericalObjectRadius:float,programMode):
    k = 0
    r = sphericalObjectRadius
    cx = centerOfSphericalObject[0]
    cy = centerOfSphericalObject[1]
    cz = centerOfSphericalObject[2]
    x1 = startOfRayPos[0]
    y1 = startOfRayPos[1]
    z1 = startOfRayPos[2]
    x2 = endOfRayPos[0]
    y2 = endOfRayPos[1]
    z2 = endOfRayPos[2]
    vx = x2-x1
    vy = y2-y1
    vz = z2-z1
    # r**2 = x**2-2x*cx+cx**2+y**2-2y*cy+cy**2+z**2-2z*2z*cz+cz**2
    # (x**2+y**2+z**2)-2(x*cx+y*cy+z*cz)+(cx**2+cy**2+cz**2)-r**2 = 0
    # k**2a - 2k*b + c - r**2 = 0
    a = (vx**2 + vy**2 + vz**2)
    b = (2*(x1 * vx + y1 * vy + z1 * vz - vx * cx - vy * cy - vz * cz))
    c = x1 * x1 - 2 * x1 * cx + cx * cx + y1 * y1 - 2 * y1 * cy + cy * cy + z1 * z1 - 2 * z1 * cz + cz * cz - r * r
    discriminant = b**2-4*a*c
    if discriminant>=0:
        k1 = (-b+math.sqrt(discriminant))/(2*a)
        k2 = (-b-math.sqrt(discriminant))/(2*a)
        if k1>k2:
            k = k2
        else:
            k = k1
        rayIntersectionPos =  (x1 + k*(vx),y1 + k*(vy),z1 + k*(vz))
        if programMode == 1:
            return rayIntersectionPos
        else: 
            if abs(x2-rayIntersectionPos[0]) > 10/scaleCoff:
                return None
            else:
                return rayIntersectionPos
    else:
        return None

def getCityLocation(cityLatitundal,earthPos:tuple,earthRadius:float,timeEphemeris:float):
    latitude = cityLatitundal[0]
    longitude = cityLatitundal[1]
    earth_sunangle = getPointLatitundal(earthPos,(0,0,0))
    sub_solar_point_position = sp.subsol("Near point","EARTH",timeEphemeris,"NONE","SUN")
    radius, subsollongitude, subsollatitude = sp.reclat(sub_solar_point_position)
    # print("subsollongitude{}".format(math.degrees(subsollongitude)))
    # print("earth_sunangle[2]{}".format(math.degrees(earth_sunangle[2])))
    zangle = earth_sunangle[2] - subsollongitude
    # print("Z-Angle{}".format(math.degrees(zangle)))
    # print("Longitude{}".format(longitude))
    # print("Latitude{}".format(latitude))
    return pointLocationOnACelestialObject(earthPos,earthRadius,math.radians(latitude),-math.radians(longitude+math.degrees(zangle)))
