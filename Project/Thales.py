import os,sys
executionDirectory = os.getcwd()
sys.path.append(executionDirectory)
from Modules.Constants.constants import executionDirectory, kernelsRelativePath
import spiceypy as sp
import time
from Modules.Eclispe_Calculations import eclipseFinder
from Modules.Tools.intro import intro
from Modules.Tools.tools import importKernels
from Modules.Console_Menu import menu
from Modules.Scene_Visualisation import Visualisator
from Modules.Tools.CustomThread import ThreadWithReturnValue
#MAIN TASKS: CREATE LOGGER
def main():
    print(time.strftime("Current date: ""%D %H:%M:%S",time.localtime()))
    importKernels(kernelsRelativePath)
    intro()
    eclipsesList = eclipseFinder.findEclipses()
    imagesDirPath = os.path.join(os.path.dirname(executionDirectory),"Rendered Images")
    renderMode = 0
    while renderMode == 0:
        eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipsesList)
        while eclipseWindow == 0:
            eclipseWindow, penumbraRadius,eclipsedCities = menu.create_UI(eclipsesList)
        renderMode = menu.chooseRenderMode()
    Visualisator.StartVisualisation(eclipseWindow,penumbraRadius,eclipsedCities,imagesDirPath,renderMode)
    sp.kclear()
    print("Kernels unloaded!")
    
if __name__ == "__main__":
    main()

    