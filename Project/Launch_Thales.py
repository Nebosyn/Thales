import os,sys
from Modules.Tools.tools import getFilePath
from Modules.Constants.constants import blenderPythonPath
pythonFilePath = getFilePath("Thales.py")
blenderExePath = getFilePath("blender.exe")
print(pythonFilePath)
print(blenderExePath)
print(blenderPythonPath)
answer = input("Run blender in background?(y/n): ").lower()
if answer == "y":
    command = f"{blenderExePath} --python  {pythonFilePath}"
elif answer == "n":
    command = f"{blenderExePath} -b --python  {pythonFilePath}"
else:
    sys.exit("Wrong input")
directoryOfPythonFiles = os.path.dirname(pythonFilePath)
os.chdir(directoryOfPythonFiles)
value = os.system(command)