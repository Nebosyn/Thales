import os,sys
executionDirectory = os.getcwd()
sys.path.append(executionDirectory)
from Modules.Constants.constants import kernelsRelativePath,eclipsesCachePath
import spiceypy as sp
import time
from Modules.Eclispe_Calculations.FindEclipses import findEclipses
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
        eclipses_dictionary = loadEclipseCache(os.path.dirname(eclipsesCachePath),"All_Eclipses.json")    
    except:    
        print("Cannot find file 'All Eclipses Json', executing eclipses search.")
        time.sleep(1)
        eclipsesList = findEclipses()
        eclipses_dictionary = createEclipsesDictionary(eclipsesList)
        createEclipseCache("All_Eclipses",eclipses_dictionary,os.path.dirname(eclipsesCachePath))
    imagesDirPath = os.path.join(executionDirectory,"Rendered Images")
    renderMode = 0
    while renderMode == 0:
        eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipses_dictionary)
        while eclipseWindow == 0:
            eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipses_dictionary)
        renderMode = menu.chooseRenderMode()
    Visualisator.StartVisualisation(eclipseWindow,penumbraRadius,eclipsedCities,imagesDirPath,renderMode)
    sp.kclear()
    print("Kernels unloaded!")
    
if __name__ == "__main__":
    main()

    