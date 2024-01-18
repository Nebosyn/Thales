from ..Constants.constants import scaleCoff
from ..Celestial_Calculations.CelestialMath import pointLocationOnACelestialObject,getPointLatitundal
import math

def createEclipseRays(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,typeOfCreation):
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
        pointOfIntersection = calculateRayIntersection(startOfRayPos,endOfRayPos,earthPos,earthRadius,1)
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
        solarEclipseCenterPos = calculateRayIntersection(sunSpecs[0],moonSpecs[0],earthSpecs[0],earthSpecs[1]/2,1)
        if solarEclipseCenterPos != None:
            penumbraRadius = calculatePenumbraRadius(moonSpecs,earthSpecs,sunSpecs)
        listOfIntersections,radiusDecrease = fullRayCast(earthSpecs,moonSpecs,sunSpecs,penumbraRadius,"Full")
        return listOfIntersections, radiusDecrease

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