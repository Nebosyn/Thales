import os,sys
import spiceypy as sp
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
                else:
                    uinput = str(uinput)
            except:
                print("Wrong input")
                return None    
        if uinput>maxuinputValue or uinput<0:
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