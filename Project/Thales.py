import os,sys
executionDirectory = os.getcwd()
sys.path.append(executionDirectory)
from Modules.Constants.constants import executionDirectory,kernelsRelativePath,eclipsesCachePath
import spiceypy as sp
import time
from Modules.Eclispe_Calculations.eclipseFinder import findEclipses2
from Modules.Tools.intro import intro
from Modules.Tools.tools import importKernels,createEclipsesDictionary,createEclipseCache,loadEclipseCache
from Modules.Console_Menu import menu
from Modules.Scene_Visualisation import Visualisator
#MAIN TASKS: CREATE LOGGER
def main():
    print(time.strftime("Current date: ""%D %H:%M:%S",time.localtime()))
    importKernels(kernelsRelativePath)
    intro()
    try:
        eclipses_dictionary = loadEclipseCache(eclipsesCachePath,"All_Eclipses")    
    except:    
        eclipsesList = findEclipses2()
        eclipses_dictionary = createEclipsesDictionary(eclipsesList)
    createEclipseCache("All_Eclipses",eclipses_dictionary,eclipsesCachePath)
    imagesDirPath = os.path.join(executionDirectory,"Rendered Images")
    renderMode = 0
    while renderMode == 0:
        eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipses_dictionary,eclipsesList)
        while eclipseWindow == 0:
            eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipses_dictionary,eclipsesList)
        renderMode = menu.chooseRenderMode()
    Visualisator.StartVisualisation(eclipseWindow,penumbraRadius,eclipsedCities,imagesDirPath,renderMode)
    sp.kclear()
    print("Kernels unloaded!")
    
if __name__ == "__main__":
    main()

    