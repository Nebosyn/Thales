import bpy
import math
from ..Constants.constants import scaleCoff
from ..Eclispe_Calculations import City_EclipseChecker
from ..Celestial_Calculations.CelestialMath import getPointLatitundal,pointLocationOnACelestialObject
from .blenderTools import *
def createAllCameras(renderCameras,earthSpecs,moonSpecs,sunSpecs,time):
    """Function to create all chosen cameras

    Args:
        renderCameras (list): Cameras specs --> ()
        earthSpecs (tuple): Tuple of earth specifications --> (pos,diameter,object name)
        moonSpecs (tuple): Tuple of moon specifications --> (pos,diameter,object name)
        sunSpecs (tuple): Tuple of sun specifications --> (pos,diameter,object name)
        time (double): Ephemeris time in J2000 Reference Frame

    Returns:
        list: Returns a list of names of created cameras.
    """
    renderCamerasNames = []
    for cameraIdentificators in renderCameras:
        cameraData = cameraDataFilter(cameraIdentificators,earthSpecs,moonSpecs,sunSpecs,time)
        renderCamerasNames.append(cameraData[2])
        createCamera(*cameraData)
    return renderCamerasNames

def cameraDataFilter(cameraIdentificator,earthSpecs,moonSpecs,sunSpecs,time):
    if cameraIdentificator[0] == "MOON":
        cameraData = (getCameraData(moonSpecs[0],earthSpecs[0],moonSpecs[1]/2,scaleCoff,f"{cameraIdentificator[0]}--{cameraIdentificator[1]}"))
    elif cameraIdentificator[0] == "SUN":
        cameraData = (getCameraData(sunSpecs[0],earthSpecs[0],sunSpecs[1]/2,scaleCoff,f"{cameraIdentificator[0]}--{cameraIdentificator[1]}"))
    else:
        cityRectangular = City_EclipseChecker.getCityLocation(cameraIdentificator[1],earthSpecs[0],earthSpecs[1]/2,time)
        cityName = cameraIdentificator[0]
        cameraData = (getCameraData(cityRectangular,sunSpecs[0],None,scaleCoff,f"{cityName}--SUN"))
    return cameraData

def createCamera(cameraLoc:tuple,cameraAngle:tuple,cameraName:str,cameraLens:float):
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW',
        location=(cameraLoc),
        rotation=(cameraAngle[0]+math.radians(90),cameraAngle[1],-cameraAngle[2]), scale=(1, 1, 1))
    bpy.context.object.data.clip_end = 100000000
    # print("Camera lens size{}".format(cameraLens))
    bpy.context.object.name = cameraName
    bpy.context.object.data.lens = cameraLens

def moveCamera(cameraLoc:tuple,angle:tuple,cameraName:str,cameraLens:float):
    setLocation(cameraLoc,cameraName)
    bpy.data.objects[cameraName].rotation_euler = (angle[0]+math.radians(90),angle[1],-angle[2])
    
def moveAllCameras(camerasIdentificators,earthSpecs,moonSpecs,sunSpecs,time,frame):
    for cameraIdentificator in camerasIdentificators:
        cameraData = cameraDataFilter(cameraIdentificator,earthSpecs,moonSpecs,sunSpecs,time)
        moveCamera(*cameraData)
        cameraName = cameraData[2]
        insertKeyframe(cameraName,frame)

def countCameraLens(cameraPos,planetPos,scaleCoff):
    cameraLensRatio = 0.001*scaleCoff
    sunPos = (0,0,0)
    if planetPos == sunPos:
        cameraLens = 450
    else:
        vector = [planetPos[0]-cameraPos[0],planetPos[1]-cameraPos[1],planetPos[2]-cameraPos[2]]
        # print("camera vector{}".format(vector))
        # print("counted camera vector{}".format(math.sqrt(vector[0]*vector[0]+vector[1]*vector[1]+vector[2]*vector[2])))
        cameraLens = math.sqrt(vector[0]*vector[0]+vector[1]*vector[1]+vector[2]*vector[2])*cameraLensRatio
    return cameraLens

def getAllCamerasData(renderCamerasIdentificators,earthSpecs,moonSpecs,sunSpecs,time):
    allCamerasData = []
    for renderCameraIdentificator in renderCamerasIdentificators:
        cameraData = cameraDataFilter(renderCameraIdentificator,earthSpecs,moonSpecs,sunSpecs,time)
        allCamerasData.append(cameraData)
    return allCamerasData

def getCameraData(mainPlanetPos:tuple,toPlanetPos:tuple,mainPlanetRadius:float,scaleCoff:int,cameraName:str):
    cameraAngle = getPointLatitundal(mainPlanetPos,toPlanetPos)
    cameraLoc = mainPlanetPos
    if mainPlanetRadius != None:
        cameraLoc = pointLocationOnACelestialObject(mainPlanetPos,mainPlanetRadius,cameraAngle[0],cameraAngle[2])
    cameraLens = countCameraLens(cameraLoc,toPlanetPos,scaleCoff)
    return (cameraLoc,cameraAngle,cameraName,cameraLens)