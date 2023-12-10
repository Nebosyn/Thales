import os,sys
from Modules.Constants.constants import blenderPythonPath,blenderPath,thalesPath
answer = input("Run blender in the background?(y/n): ").lower()
if answer == "y":
    command = f"{blenderPath} --python  {thalesPath}"
elif answer == "n":
    command = f"{blenderPath} -b --python  {thalesPath}"
else:
    sys.exit("Wrong input")
value = os.system(command)