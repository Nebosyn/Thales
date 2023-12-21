import os,sys
import spiceypy as sp
import json
import datetime
def getFilePath(fileName):
    rootDirectory = os.getcwd()
    for relativePath,dirs,files in os.walk(rootDirectory):
        if(fileName in files):
            filePath = os.path.join(rootDirectory ,relativePath,fileName)
            return(filePath)
    sys.exit(f"{fileName} not found.")

def inputControl(userInput,maxuinputValue,listScanMode):
    if type(userInput) == list:
        for uinput in userInput:
            try:
                if listScanMode == 1:
                    uinput = int(uinput)
                    if uinput>maxuinputValue or uinput<0:
                        print("Wrong input")
                        return None
                else:
                    if type(uinput) != str:
                        print(f"-> {uinput} incorrect type")
            except:
                print("Wrong input")
                return None
    else:
        try:    
            userInput = int(userInput)
        except:
            print("Wrong input")
            return None
        if userInput>maxuinputValue or userInput<0:
            print("Wrong input")
            return None
    return userInput

def createEclipseCache(fileName,valueToWrite,pathToFile):
    with open(pathToFile+"\\"+fileName+".json","w") as f:
        json.dump(valueToWrite,f)

def createEclipsesDictionary(eclipses_list):
    eclipses_dictionary = {}
    for eclipse in eclipses_list:
        eclipsestrp_start = datetime.datetime.strptime(eclipse[0],"%Y %b %d %H:%M:%S")  
        eclipsestrp_end = datetime.datetime.strptime(eclipse[1],"%Y %b %d %H:%M:%S")  
        # print(eclipsestrp_start)
        year_century = str(eclipsestrp_start.year)[:-2]
        if year_century not in eclipses_dictionary.keys():
            eclipses_dictionary[year_century] = []
        eclipses_dictionary[year_century].append(eclipse)
    return eclipses_dictionary

def loadEclipseCache(fileDirPath,fileName):
    with open(f"{os.path.join(fileDirPath,fileName)}","r") as f:
        dicitonary =json.load(f)
        return dicitonary

def importKernels(kernelsRelativePath):
    programExecutionDir = os.getcwd()
    print("Spice Version: " + sp.tkvrsn("Toolkit"))
    print("Searching for kernels...")
    metaKernel = "meta-kernel.txt"
    kernelsPath = os.path.join(programExecutionDir,kernelsRelativePath)
    try:
        print(kernelsPath)
        metaKernelPath = os.path.join(kernelsPath,metaKernel)
        os.chdir(kernelsPath)
    except:
        metaKernelPath = getFilePath(metaKernel)
        os.chdir(kernelsPath)  
    with open(metaKernelPath,"r") as file:
        kernelsList = (file.read().split("(")[1]).split(")")[0]
        print ("Loading kernels:")
        sp.furnsh(metaKernelPath)
        print(kernelsList)
        print("Kernels loaded!")
    os.chdir(programExecutionDir)

def imagePathNamer(time,imagesDirPath,cameraName):
    imagesDirPath = os.path.join(imagesDirPath,cameraName)
    imageName = cameraName + " " + str(sp.et2utc(time,"C",0).replace(":","-"))
    imageSavePath = os.path.join(imagesDirPath,imageName)
    return imageSavePath,imageName