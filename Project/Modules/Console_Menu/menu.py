import os,sys
import spiceypy as sp
import datetime
from ..Eclispe_Calculations import eclipseFinder,City_EclipseChecker
from ..Constants.constants import  scaleCoff,eclipsesCachePath
from ..Tools.tools import inputControl, createEclipseCache, loadEclipseCache, createEclipsesDictionary, loading_bar
def create_UI(eclipses_dictionary):
    print("""
1.All eclipses
2.Eclipses by country
0.Exit Thales""")
    output = 0
    while output == 0:
        global programMode
        programMode = inputControl(input("Select program mode: "),2,None)
        if programMode != None:
            break
    if programMode == 1:
        output = centuriesMenu(eclipses_dictionary)
        while output[1] == 0:
            output = centuriesMenu(eclipses_dictionary)
        return output
    elif programMode == 2:
        loop = True
        while loop:
            sortedEclipsesFiles = os.listdir(eclipsesCachePath)
            for index,sortedEclipsesFile in enumerate(sortedEclipsesFiles):
                countryName = sortedEclipsesFile.split(".")[0]
                if countryName == "All Eclipses":
                    index-=1
                    continue
                print(f"{index+1}. {countryName}")
            print("Available countries")
            while True:
                userInput = input("Choose country (Need another country? Type: Recalculate): ")
                if userInput.lower() == "recalculate": 
                    try:
                        chosenCountry = chooseCountries(1)
                        eclipses_dictionary = sortEclipsesByCountry(eclipses_dictionary,chosenCountry)
                        loop = False
                        break
                    except:
                        sys.exit("Program Crashed")
                else:
                    userInput = inputControl(userInput,index+1,None)
                    eclipses_dictionary = loadEclipseCache(eclipsesCachePath,sortedEclipsesFiles[userInput-1])
                    loop = False
                    break
        output = centuriesMenu(eclipses_dictionary)
        while output[1] == 0:
            output = centuriesMenu(eclipses_dictionary)
        return output
    elif programMode == 0:
        sys.exit("Exiting Thales")

def sortEclipsesByCountry(eclipses_dictionary,chosenCountry):
    
    eclipses_list = [] 
    for i in eclipses_dictionary.values():
        eclipses_list += i 
    eclipses_list_certain_country = []
    for index, eclipse in enumerate(eclipses_list):
        loading_bar(index, len(eclipses_list),20)
        print(f"{index} of {len(eclipses_list)} eclipses scanned")
        recalculated_eclipse, penumbraRadius = eclipseFinder.recalculateEclipse(eclipse)
        if City_EclipseChecker.citiesEclipseCheck(recalculated_eclipse,scaleCoff,4,penumbraRadius,chosenCountry) == True:
            eclipses_list_certain_country.append(recalculated_eclipse)
            print(f"Country was eclipsed, adding eclipse window (№{index+1}) to the list")
            continue
    eclipses_dictionary = createEclipsesDictionary(eclipses_list_certain_country)
    createEclipseCache(chosenCountry,eclipses_dictionary,eclipsesCachePath)
    return eclipses_dictionary



def centuriesMenu(eclipses_dictionary):
    print("Select desired century:")
    for index,century in enumerate(eclipses_dictionary.keys()):
        print(f"{index+1}.{century}00")
    print("0.Change program mode")
    while True:
        menuInput = inputControl(input("Choose a number: "),index+1,None)
        if menuInput != None: 
            break
    if menuInput == 0:
        return 0,1,1
    output = eclipsesOfCenturyMenu(list(eclipses_dictionary.keys())[menuInput-1],eclipses_dictionary)
    while output[2] == 0: 
        output = eclipsesOfCenturyMenu(list(eclipses_dictionary.keys())[menuInput-1],eclipses_dictionary)
    return output

def eclipsesOfCenturyMenu(chosenCentury,eclipses_dictionary):
    for index, eclipseWindow in enumerate(eclipses_dictionary[chosenCentury]):
        eclipse_without_time = (" ".join(eclipseWindow[0].split()[:3])," ".join(eclipseWindow[1].split()[:3]))
        durationOfEclipse = str(datetime.timedelta(seconds = sp.utc2et(eclipseWindow[1])-sp.utc2et(eclipseWindow[0]))).split('.')[0]
        print(f"{index+1}. {eclipse_without_time[0]}")
    print("0.Change century")
    print(f"Chosen century -- {chosenCentury}")
    windowNumber = inputControl(input("Select eclipse from the list: "),index+1,None)
    while True:
        if windowNumber != None:
            break
    if windowNumber == 0:
        return 1,0,1
    chosen_eclipse = eclipses_dictionary.get(chosenCentury)[windowNumber-1]
    chosen_eclipse,penumbraRadius, eclipsedCities = cityScan(chosen_eclipse)
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
        cityScanMode = inputControl(input("Chose city scan mode:"),3,None)
        if cityScanMode != None:
            break
    if cityScanMode == 0:
        return 1, 1, 0
    chosenCountries = None
    if cityScanMode == 3:
        print()
        print(f"Chosen eclipse : {chosen_eclipse[0]} -- {chosen_eclipse[1]}")
        chosenCountries = chooseCountries(2)
    eclipsedCities = City_EclipseChecker.citiesEclipseCheck(chosen_eclipse,scaleCoff,cityScanMode,penumbraRadius,chosenCountries)
    return chosen_eclipse,eclipsedCities, penumbraRadius

def chooseRenderMode():
    whatToDo = inputControl(input(
"""1.Create animation
0.Rechoose eclipse
Choose option: """),2,None)
    return whatToDo

def chooseCountries(countryChooseMode):
    currentPath = os.getcwd()
    availableCountries = City_EclipseChecker.getAvailableCountries()
    availableCountries = sorted(availableCountries,key=str.lower)
    for index,country in enumerate(availableCountries):
        print(f"{index+1}. {country}")
    if countryChooseMode == 2:
        print("0. Change city scan mode")
    while True:
        try:
            if countryChooseMode == 1:
                chosenCountryNumber = inputControl(input(f"Please choose country number (Sorting will take about 30-40 minutes): "),index+1,None)
                chosenCountries = availableCountries[int(chosenCountryNumber)-1]
            elif countryChooseMode == 2:
                chosenCountries = []
                chosenCountriesNumbers = inputControl(input(f"Please choose country/countries in the list(Separated by commas): ").split(","),index+1,None)
                chosenCountriesNumbers.sort()
                if chosenCountriesNumbers[0] == 0:
                        return 0, 0, 0
                for chosenCountryNumber in chosenCountriesNumbers:
                    chosenCountries.append(availableCountries[int(chosenCountryNumber)-1])
            os.chdir(currentPath)
            break
        except:
            print("Wrong input")
    return chosenCountries

def chooseCameras(eclipsedCities):
    renderCamerasIdentificators = []
    eclipsedCities = sorted(eclipsedCities, key= lambda x: x[0])
    defaultCameras = [("MOON","EARTH"),("SUN","EARTH")]
    
    [print(f"{index+1}. {cameraData[0]}--SUN") for index,cameraData in enumerate(eclipsedCities)]
    print("Cameras in space\n")
    [print(f"{len(eclipsedCities)+index+1}. {cameraData[0]}--{cameraData[1]}") for index,cameraData in enumerate(defaultCameras)]
    print("0. Choose all cameras (The rendering process for all cameras is expected to take a minimum of 1-3 hours.)")
    availableCameras = eclipsedCities+defaultCameras
    renderCamerasIdentificatorsNumbers = input("Choose cameras(Separated by commas: 1,2,3...): ").split(",")
    renderCamerasIdentificatorsNumbers.sort()
    if int(renderCamerasIdentificatorsNumbers[0]) == 0:
        renderCamerasIdentificators = availableCameras
    else:
        for cameraNumber in renderCamerasIdentificatorsNumbers: 
            renderCamerasIdentificators.append(availableCameras[int(cameraNumber)-1])
    return renderCamerasIdentificators