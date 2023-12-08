import math
import spiceypy as sp

def getPointLatitundal(frompos,topos):
    return (math.atan2((topos[2]-frompos[2]),(math.hypot(topos[0]-frompos[0],topos[1]-frompos[1]))),0,
           math.atan2((topos[0]-frompos[0]),(topos[1]-frompos[1])))
    
def pointLocationOnACelestialObject(planetPos,planetRadius,xangle,zangle):
    # print("CAMERALOC")
    # print("x-angle{}".format(math.degrees(xangle)))
    # print("z-angle{}".format(math.degrees(zangle)))
    # print("diameter{}".format(planetRadius*2))
    # print("planet Pos {}".format(planetPos))
    xy= math.cos(xangle)*planetRadius
    x = math.sin(zangle)*xy
    y = math.cos(zangle)*xy
    z = math.sin(xangle)*planetRadius
    return (x+planetPos[0],y+planetPos[1],z+planetPos[2])    

def convertSunEclipsePos(solarEclipsePosbySun,earthPos,scaleCoff):
    solarEclipsePosbyEarth = []
    print("solarEclipsePosbySun{}".format(solarEclipsePosbySun))
    print("earthPos{}".format(earthPos))
    for i in range(3):
        solarEclipsePosbyEarth.append((solarEclipsePosbySun[i]-earthPos[i]))
    print("suneclipse pos:{}".format(solarEclipsePosbyEarth))
    return solarEclipsePosbyEarth

def calculateObjectRotation(planetName:str,time:float,planetPos:tuple,sunPos:tuple):
    mainPlanet_sunAngle = getPointLatitundal(planetPos,sunPos)
    sub_solar_point_position = sp.subsol("Near point",planetName,time,"NONE","SUN")
    # print("Sub Sol:{} {}".format(sub_solar_point_position,planetName))
    [radius, longitude, latitude] = sp.reclat(sub_solar_point_position)
    # print("Sub Sol: long:{} lat:{} planet:{}".format(math.degrees(longitude),math.degrees(latitude),planetName))
    zangle = -mainPlanet_sunAngle[2] - longitude
    return zangle