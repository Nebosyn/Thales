from zipfile import ZipFile
import os
root_directory = os.getcwd()
print(root_directory)
("Astronomy Project","zip",root_directory)
with ZipFile(root_directory+"\\Astronomy Project.zip","w") as zipfile:
    zipfile.write("City_EclipseChecker.py")
    zipfile.write("eclipsefinder.py")
    zipfile.write("SolarEclipseVisualisator.py")
    zipfile.write("positionCalculator.py")
    zipfile.write("menu.py")
    zipfile.write("tools.py")