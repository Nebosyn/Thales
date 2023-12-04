import os,sys
import spiceypy as sp
import datetime
from ..Eclispe_Calculations import eclipseFinder,City_EclipseChecker
from ..Constants.constants import  scaleCoff
from ..Tools.tools import inputControl

def create_UI(eclipses_list):
    eclipses_dictionary = {}
    print("""
1.All eclipses
2.Eclipses for desired city/cities
3.Manual date input """)
    while True:
        programMode = inputControl(input("Select program mode: "),3)
        if programMode != None:
            break
    if programMode == 1:
        for eclipse in eclipses_list:
            eclipsestrp_start = datetime.datetime.strptime(eclipse[0],"%Y %b %d %H:%M:%S")  
            eclipsestrp_end = datetime.datetime.strptime(eclipse[1],"%Y %b %d %H:%M:%S")  
            print(eclipsestrp_start)
            year_century = str(eclipsestrp_start.year)[:-2]
            if year_century not in eclipses_dictionary.keys():
                eclipses_dictionary[year_century] = []
            eclipses_dictionary[year_century].append(eclipse)
        print(eclipses_dictionary)
        output = centuriesMenu(eclipses_dictionary)
        while output[1] == 0:
            output = centuriesMenu(eclipses_dictionary)
        return output
    elif programMode == 2:
        userInput = input("Enter city/cities separated by commas: ")
        try:
            citiesList = userInput.split(",")
        except:
            sys.exit("Error occured")
        
def centuriesMenu(eclipses_dictionary):
    print("Select desired century:")
    for index,century in enumerate(eclipses_dictionary.keys()):
        print(f"{index+1}.{century}00")
    print("0.Change program mode")
    while True:
        menuInput = inputControl(input("Choose a number: "),index+1)
        if menuInput != None: 
            break
    if menuInput == 0:
        return 0,1,1
    output = eclipsesOfCenturyMenu(list(eclipses_dictionary.keys())[menuInput-1],eclipses_dictionary)
    while output[2] == 0: 
        output = eclipsesOfCenturyMenu(list(eclipses_dictionary.keys())[menuInput-1],eclipses_dictionary)
    return output

def eclipsesOfCenturyMenu(chosenCentury,eclipses_dictionary):
    print(chosenCentury)
    print(type(chosenCentury))
    for index, eclipseWindow in enumerate(eclipses_dictionary[chosenCentury]):
        eclipse_without_time = (" ".join(eclipseWindow[0].split()[:3])," ".join(eclipseWindow[1].split()[:3]))
        durationOfEclipse = str(datetime.timedelta(seconds = sp.utc2et(eclipseWindow[1])-sp.utc2et(eclipseWindow[0]))).split('.')[0]
        print(f"{index+1}. {eclipse_without_time[0]}")
    print("0.Change century")
    windowNumber = inputControl(input("Select eclipse from the list: "),index+1)
    while True:
        if windowNumber != None:
            break
    if windowNumber == 0:
        return 1,0,1
    chosen_eclipse = eclipses_dictionary.get(chosenCentury)[windowNumber-1]
    chosen_eclipse,penumbraRadius, eclipsedCities= cityScan(chosen_eclipse)
    return chosen_eclipse,eclipsedCities,penumbraRadius

def cityScan(chosen_eclipse):
    chosen_eclipse,penumbraRadius = eclipseFinder.recalculateEclipse(chosen_eclipse)
    print(f"Chosen eclipse : {chosen_eclipse[0]} -- {chosen_eclipse[1]}")
    print("""
1.Only capitals
2.Capitals and primary cities
3.Certain countries
0.Rechoose eclipse""")
    while True: 
        cityScanMode = inputControl(input("Chose city scan mode:"),3)
        if cityScanMode != None:
            break
    if cityScanMode == 0:
        return 1, 1, 0
    chosenCountries = None
    if cityScanMode == 3:
        currentPath = os.getcwd()
        availableCountries = City_EclipseChecker.getAvailableCountries()
        for index,country in enumerate(availableCountries):
            print(f"{index+1}. {country}")
        print("0. Change city scan mode")
        while True:
            try:
                chosenCountries = []
                chosenCountriesNumbers = inputControl(input(f"Please choose countires in the list(Separated by commas): ").split(","),index+1)
                chosenCountriesNumbers.sort()
                if chosenCountryNumber[0] == 0:
                        return 0, 0, 0
                for chosenCountryNumber in chosenCountriesNumbers:
                    chosenCountries.append(availableCountries[int(chosenCountryNumber)-1])
                os.chdir(currentPath)
                break
            except:
                print("Wrong input")
    eclipsedCities = City_EclipseChecker.CityEclipseCheck(chosen_eclipse,scaleCoff,cityScanMode,penumbraRadius,chosenCountries)
    return chosen_eclipse,eclipsedCities, penumbraRadius

def chooseRenderMode():
    whatToDo = inputControl(input(
"""Choose option
1.Create animation
2.Render a photo
0.Rechoose eclipse
: """),2)
    return whatToDo

def chooseCameras(eclipsedCities):
    renderCamerasIdentificators = []
    
    defaultCameras = [("MOON","EARTH"),("SUN","EARTH")]
    availableCameras = eclipsedCities+defaultCameras
    
    [print(f"{index+1}. {cameraData[0]}--SUN") for index,cameraData in enumerate(availableCameras)]   
    
    renderCamerasIdentificatorsNumbers = input("Choose cameras(Separated by commas): ").split(",")
    renderCamerasIdentificatorsNumbers.sort()
    if int(renderCamerasIdentificatorsNumbers[0]) == 0:
        renderCamerasIdentificators = availableCameras
    else:
        for cameraNumber in renderCamerasIdentificatorsNumbers: 
            renderCamerasIdentificators.append(availableCameras[int(cameraNumber)-1])
    return renderCamerasIdentificators