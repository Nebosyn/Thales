import bpy
import os
import datetime
import spiceypy as sp
from ..Constants.constants import scaleCoff,step, videoSpeed
from ..Eclispe_Calculations.eclipseFinder import createEclipseShadowMapping
from ..Celestial_Data.data import getCelestialObjectSpecs
from ..Tools.tools import getFilePath,imagePathNamer
from ..Console_Menu.menu import chooseCameras
from .blenderTools import *
from .CameraManipulate import *
def StartVisualisation(eclipseWindow,penumbraRadius,eclipsedCities,imagesDirPath,renderMode:int):
    
    clean_scene()
    
    start_utc = eclipseWindow[0]
    end_utc = eclipseWindow[1]
    #Convert UTC to ET
    start_ephemerisTime = sp.str2et(start_utc)
    end_ephemerisTime = sp.str2et(end_utc)
    
    quantityOfFrames = int(((end_ephemerisTime-start_ephemerisTime)//step)+1)
    
    moonSpecs = getCelestialObjectSpecs("MOON",start_ephemerisTime,scaleCoff)
    earthSpecs = getCelestialObjectSpecs("EARTH",start_ephemerisTime,scaleCoff)
    sunSpecs = getCelestialObjectSpecs("SUN",start_ephemerisTime,scaleCoff)
    moonSpecs = getCelestialObjectSpecs("MOON",start_ephemerisTime,scaleCoff)
    earthSpecs = getCelestialObjectSpecs("EARTH",start_ephemerisTime,scaleCoff)
    sunSpecs = getCelestialObjectSpecs("SUN",start_ephemerisTime,scaleCoff)

    earthModelPath = getFilePath("Earth_1_12756.glb")
    moonModelPath = getFilePath("Moon_1_3474.glb")
    sunModelPath = getFilePath("Sun_1_1391000.glb")

    # import sun
    createCelestialObject(sunModelPath,sunSpecs[2],sunSpecs,start_ephemerisTime,sunSpecs[0])
    createCelestialObject(moonModelPath,moonSpecs[2],moonSpecs,start_ephemerisTime,sunSpecs[0])
    createCelestialObject(earthModelPath,earthSpecs[2],earthSpecs,start_ephemerisTime,sunSpecs[0])
    
    setRenderProperties()
    createLight(sunSpecs[1]/4)
    renderCamerasIdentificators = chooseCameras(eclipsedCities)
    renderCamerasNames = createAllCameras(renderCamerasIdentificators,earthSpecs,moonSpecs,sunSpecs,start_ephemerisTime)
    if renderMode == 1:
        renderAnimation(start_ephemerisTime,renderCamerasIdentificators,renderCamerasNames,sunSpecs,imagesDirPath,step,quantityOfFrames,scaleCoff,penumbraRadius)

def renderAnimation(start_ephemerisTime:float,renderCamerasIdentificators:list,renderCamerasNames:list,sunSpecs:list,imagesDirPath:str,step:int,quantityOfFrames:int,scaleCoff:int,penumbraRadius):
    imagesDirPath,end_utc_time,timeToRenderVideos,videoSpeed = createFrames(start_ephemerisTime,renderCamerasIdentificators,renderCamerasNames,sunSpecs,imagesDirPath,step,quantityOfFrames,scaleCoff,penumbraRadius)
    if input(f"Render Videos?(Approximate time of render:{timeToRenderVideos}) y/n: ").lower()== "y":
        configureVideoEditor(imagesDirPath,renderCamerasNames,videoSpeed)
        renderVideo(start_ephemerisTime,end_utc_time,imagesDirPath,renderCamerasNames)

def createFrames(start_ephemerisTime:float,renderCamerasIdentificators:list,renderCamerasNames,sunSpecs:list,imagesDirPath:str,step:int,quantityOfFrames:int,scaleCoff:int,penumbraRadius):
    print("Calculating...")
    imagesDirPath = os.path.join(imagesDirPath,(str(sp.et2utc(start_ephemerisTime,"C",0).replace(":","-"))))
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_current = 0
    scene.frame_end = quantityOfFrames
    bpy.context.scene.render.fps = 60
    frameRenderDate = start_ephemerisTime
    scene.render.image_settings.file_format = 'PNG' 
    for frame in range(quantityOfFrames):
        moonSpecs = getCelestialObjectSpecs("MOON",frameRenderDate,scaleCoff)
        earthSpecs = getCelestialObjectSpecs("EARTH",frameRenderDate,scaleCoff)
        # print("x ",cityPosition[0]-earthSpecs[0][0])
        # print("y ",cityPosition[1]-earthSpecs[0][1])
        # print("z ",cityPosition[2]-earthSpecs[0][2])
        # print("x ",solarEclipsePos[0]-earthSpecs[0][0])
        # print("y ",solarEclipsePos[1]-earthSpecs[0][1])
        # print("z ",solarEclipsePos[2]-earthSpecs[0][2])
        # print("radius of earth ",earthSpecs[1]/2)
        movePlanet(earthSpecs[2],earthSpecs,frameRenderDate,sunSpecs[0])
        insertKeyframe(earthSpecs[2],frame)
        movePlanet(moonSpecs[2],moonSpecs,frameRenderDate,sunSpecs[0])
        insertKeyframe(moonSpecs[2],frame)
        moveAllCameras(renderCamerasIdentificators,earthSpecs,moonSpecs,sunSpecs,frameRenderDate,frame)
        listOfIntersections, radiusOfDecrease = createEclipseShadowMapping(earthSpecs,moonSpecs,sunSpecs,penumbraRadius)
        createEclipseMap(listOfIntersections,frame)
        frameRenderDate += step
    createIcosphere(radiusOfDecrease)
    end_utc_time = str(sp.et2utc(frameRenderDate,"C",0).replace(":","-"))
    createSkybox()
    amountOfCameras = len(renderCamerasNames)
    amountOfAllFrames,timeToRenderFrames,timeToRenderVideos = renderData(amountOfCameras,quantityOfFrames,videoSpeed)
    allCamerasData = getAllCamerasData(renderCamerasIdentificators,earthSpecs,moonSpecs,sunSpecs,frameRenderDate)
    print("Done")
    if input(f"Render frames? (Amount of frames: {amountOfAllFrames}; Approximate time of render: {timeToRenderFrames}) y/n: ").lower() == "y":
        bpy.context.scene.render.use_stamp_note = True
        renderFrames(start_ephemerisTime,quantityOfFrames,allCamerasData,imagesDirPath,step)
    return imagesDirPath,end_utc_time,timeToRenderVideos,videoSpeed



def renderData(amountOfCameras,amountOfFrames,videoSpeed):
    approximateTimeToRenderOneFrame = 0.25
    approximateTimeToAppendOneFrame = 0.10
    amountOfAllFrames = amountOfCameras*amountOfFrames
    timeToRenderFrames = str(datetime.timedelta(seconds = amountOfAllFrames*approximateTimeToRenderOneFrame))
    timeToRenderVideos = str(datetime.timedelta(seconds = (amountOfAllFrames/(videoSpeed/100))*approximateTimeToAppendOneFrame))
    return amountOfAllFrames,timeToRenderFrames,timeToRenderVideos

def renderFrames(renderDateTime,quantityOfFrames,camerasData,imagesDirPath,step):
    for frame in range(quantityOfFrames):
        bpy.context.scene.frame_current = frame
        for cameraData in camerasData:
            cameraName = cameraData[2]
            shadowMap = bpy.data.objects.get(f'EclipseShadowMap{frame}')
            if shadowMap != None and cameraName == "MOON--EARTH":
                parentIcosphere(frame)
            renderFrame(renderDateTime,imagesDirPath,cameraData)
        renderDateTime += step

def renderFrame(time,imagesDirPath,cameraData):
    cameraName = cameraData[2]
    cameraLens = cameraData[3]    
    imageSavePath,imageName = imagePathNamer(time,imagesDirPath,cameraName)
    bpy.context.scene.render.stamp_note_text = str(sp.et2utc(time,"C",0))
    print(str(sp.et2utc(time,"C",0)))
    skybox_starsnoise_value(cameraLens)
    bpy.context.scene.camera = bpy.data.objects[cameraName]
    bpy.context.scene.render.filepath = imageSavePath
    bpy.ops.render.render(write_still=True)
