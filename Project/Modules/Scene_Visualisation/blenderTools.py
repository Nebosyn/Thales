import bpy
import os
import spiceypy as sp
from ..Celestial_Calculations.CelestialMath import  calculateObjectRotation
import time
def insertKeyframe(objectName,frame):
    bpy.context.scene.objects[objectName].keyframe_insert(data_path='location',frame=frame)
    bpy.context.scene.objects[objectName].keyframe_insert(data_path='rotation_euler',frame=frame)
    
def setLocation(objectPos:tuple,objectName:str):
    bpy.data.objects[objectName].location = objectPos
    
def setSize(objectDiameter:float):
    bpy.context.object.dimensions.xyz = (objectDiameter,objectDiameter,objectDiameter)
    
def createLight(sunRadius:float):
    bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.energy = 2e+08
    bpy.context.object.data.use_contact_shadow = True
    bpy.context.object.data.shadow_soft_size = sunRadius
    bpy.context.object.data.contact_shadow_distance = 9999
    
def setRenderProperties():
    bpy.context.scene.render.use_stamp_date = False
    bpy.context.scene.render.use_stamp_time = False
    bpy.context.scene.render.use_stamp_render_time = False
    bpy.context.scene.render.use_stamp_frame = False
    bpy.context.scene.render.use_stamp_camera = True
    bpy.context.scene.render.use_stamp_scene = False
    bpy.context.scene.render.use_stamp_filename = False
    bpy.context.scene.render.use_stamp_note = True
    bpy.context.scene.render.use_stamp = True
    bpy.context.scene.render.stamp_font_size = 64
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.shadow_cube_size = '4096'
    bpy.context.scene.eevee.shadow_cascade_size = '4096'
    bpy.context.scene.eevee.use_shadow_high_bitdepth = True
    bpy.context.scene.eevee.use_soft_shadows = False
    bpy.context.scene.render.use_high_quality_normals = True
    bpy.data.objects["SUN"].active_material.shadow_method = 'NONE'
    bpy.context.scene.eevee.taa_render_samples = 1

def clean_scene():
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge(do_local_ids = True, do_linked_ids = True, do_recursive = True)

def renderImage(cameraName:str,saveFolderPath:str,fileName:str):
    bpy.context.scene.camera = bpy.data.objects[cameraName]
    bpy.context.scene.render.filepath = os.path.join(saveFolderPath,fileName+" "+cameraName)
    start = time.time()
    bpy.ops.render.opengl(write_still = True)
    end = time.time()
    print(f"Picture saved, wasted time: {start-end} seconds")
    
def configureVideoEditor(imagesDirPath,renderCamerasNames,videoSpeed):
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    # print("ImagesDirPath{}".format(imagesDirPath))
    sequencer = bpy.context.scene.sequence_editor
    channelCounter = 1
    for cameraName in renderCamerasNames:
        # print(*renderCamerasNames)
        imagesFolder = os.path.join(imagesDirPath,cameraName)
        imagesList = sorted(os.listdir(imagesFolder))
        firstImage, *restImages = imagesList
        firstImagePath = os.path.join(imagesFolder,firstImage)
        imagesStrip = sequencer.sequences.new_image(
            name=firstImage,
            filepath=firstImagePath,
            channel=channelCounter,
            frame_start=0,
            fit_method='ORIGINAL'
        )
        bpy.context.scene.sequence_editor.channels[f"Channel {channelCounter}"].name = cameraName
        bpy.context.scene.sequence_editor.channels[cameraName].mute = True
        for image in restImages:
            imagesStrip.elements.append(image)
        channelCounter += 1
    bpy.context.scene.frame_end = bpy.data.scenes['Scene'].sequence_editor.sequences_all[firstImage].frame_final_end
    bpy.context.scene.render.use_stamp_note = False
    bpy.context.scene.render.use_stamp = False
    bpy.context.scene.render.use_stamp_camera = False

def renderVideo(start_ephemerisTime,end_utc_time,imagesDirPath,camerasNames):
    start_utc_time = str(sp.et2utc(start_ephemerisTime,"C",0).replace(":","-"))
    videosSaveFolderPath = os.path.join(imagesDirPath,"Rendered Videos")
    reversed(camerasNames)
    for cameraName in camerasNames:
        if cameraName == "Rendered Videos":
            continue
        bpy.context.scene.sequence_editor.channels[cameraName].mute = False
        videoSavePath = os.path.join(videosSaveFolderPath,cameraName+f" {start_utc_time} -- {end_utc_time}")
        bpy.context.scene.render.filepath = videoSavePath
        bpy.ops.render.render(animation = True,write_still = True)
        bpy.context.scene.sequence_editor.channels[cameraName].mute = True
        
def createIcosphere(radiusOfDecrease):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radiusOfDecrease, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    icosphere = bpy.data.objects['Icosphere']
    material = bpy.data.materials.new("Icosphere shading")
    material.use_nodes = True
    nodesDeck = material.node_tree.nodes
    principledBSDF = nodesDeck['Principled BSDF']
    principledBSDF.inputs['Base Color'].default_value = (0.0, 0, 0, 1.0)
    principledBSDF.inputs['IOR'].default_value = 0
    principledBSDF.inputs['Specular IOR Level'].default_value = 0
    principledBSDF.inputs['Roughness'].default_value = 0
    principledBSDF.inputs['Sheen Tint'].default_value = (1,1,1,1)
    principledBSDF.inputs['Coat Roughness'].default_value = 0
    principledBSDF.inputs['Alpha'].default_value = 0.2
    material.blend_method = 'BLEND'
    icosphere.data.materials.append(material)
    
def skybox_starsnoise_value(cameraLens):
    skybox_cameraRatio = 2.382007900326203
    noise_value = skybox_cameraRatio*cameraLens
    bpy.data.worlds["World"].node_tree.nodes["Noise Texture"].inputs[2].default_value = noise_value
    
def createSkybox():
    nodesDeck = bpy.data.worlds["World"].node_tree
    nodesDeck.nodes.new(type="ShaderNodeTexNoise")
    nodesDeck.nodes.new(type="ShaderNodeValToRGB")
    backgroundInputColor = nodesDeck.nodes['Background'].inputs['Color']
    noiseTextureOutputColor = nodesDeck.nodes['Noise Texture'].outputs['Color']
    colorRampInputFax = nodesDeck.nodes['Color Ramp'].inputs['Fac']
    colorRampOutputColor = nodesDeck.nodes['Color Ramp'].outputs['Color']
    nodesDeck.links.new(backgroundInputColor,colorRampOutputColor,verify_limits = True)
    nodesDeck.links.new(colorRampInputFax,noiseTextureOutputColor,verify_limits = True)
    nodesDeck.nodes['Color Ramp'].color_ramp.elements[1].position = 0.709091
    nodesDeck.nodes['Color Ramp'].color_ramp.interpolation = 'CONSTANT'
    nodesDeck.nodes['Color Ramp'].color_ramp.elements[1].color[0] = 1.000
    nodesDeck.nodes['Color Ramp'].color_ramp.elements[1].color[1] = 0.939
    nodesDeck.nodes['Color Ramp'].color_ramp.elements[1].color[2] = 0.631
    nodesDeck.nodes["Noise Texture"].inputs[2].default_value = 500
    # bpy.data.images.load(skyboxPath)
    # nodesDeck.nodes.new(type="ShaderNodeTexEnvironment")
    # skyboxOutput = nodesDeck.nodes['Environment Texture'].outputs['Color']
    # tex = bpy.data.images.get('skybox.exr')
    # nodesDeck.nodes['Environment Texture'].image = tex
    # nodesDeck.links.new(backgroundInputColor,skyboxOutput)

def createEclipseMap(pointsLists,frame):
    vertes = []
    lengthsOfLists = []
    for pointsList in pointsLists:
        lengthsOfLists.append(len(pointsList))
        for points in pointsList:
            vertes.append(points)
    numberOfPointsInList = len(pointsLists)
    indexedPoints = list(range(len(vertes)))
    # groupedNumberOfPointsList = chunker(indexedPoints,lengthsOfLists)
    # print(vertes)
    edges = []
    faces = []
    meshData = bpy.data.meshes.new("EclipseOutline")
    meshData.from_pydata(vertes,edges,faces)
    eclipseOutlineObject = bpy.data.objects.new(f'EclipseShadowMap{frame}',meshData)
    bpy.context.collection.objects.link(eclipseOutlineObject)
    eclipseOutlineName = eclipseOutlineObject.name_full
    bpy.data.objects[eclipseOutlineName].instance_type = "VERTS"
    
def movePlanet(planetName:str,planetSpecs:list,ephemerisTime:float,sunPos:tuple):
    if planetName !="SUN":
        setPlanetRotation(planetName,ephemerisTime,planetSpecs[0],sunPos)
    setLocation(planetSpecs[0],planetName)

def setPlanetRotation(planetName:str,time:float,planetPos:tuple,sunPos:tuple):
    zangle = calculateObjectRotation(planetName,time,planetPos,sunPos)
    bpy.context.object.rotation_mode = 'XYZ'
    bpy.data.objects[planetName].rotation_euler = (0,0,zangle)
    
def createCelestialObject(planetFilepath:str,planetName:str,planetSpecs:list,time:float,sunPos:tuple):
    bpy.ops.import_scene.gltf(filepath=planetFilepath)
    bpy.context.object.name = planetName
    movePlanet(planetName,planetSpecs,time,sunPos)
    setSize(planetSpecs[1])

def parentIcosphere(frame):
    eclipseMappingObject = bpy.data.objects[f'EclipseShadowMap{frame}']
    icosphere = bpy.data.objects['Icosphere']
    icosphere.parent = eclipseMappingObject
