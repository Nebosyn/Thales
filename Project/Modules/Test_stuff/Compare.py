import csv,os,json

def loadEclipseCache(fileDirPath,fileName):
    with open(f"{os.path.join(fileDirPath,fileName)}","r") as f:
        dicitonary = json.load(f)
        return dicitonary
    
def compare_by_century(century,fileName):
    with open(f"Project\\Modules\\Test_stuff\\{fileName}") as f:
        eclipses_dict = list(csv.reader(f))
        MyEclipses = loadEclipseCache("Project\\Modules\\Test_stuff", "All_Eclipses.json")
        print(f"CENTURY {century}")
        print(f"NASA Eclipses {len(eclipses_dict)} , My Eclipses {len(MyEclipses[str(century)])}")
        trueCounter = 0
        falseCounter = 0
        false_eclipse_dates = []
        secondOptionCounter = 0
        for myEclipse in MyEclipses[str(century)]:
            My_eclipse_date_start = myEclipse[0].split(" ")
            My_eclipse_date_start = My_eclipse_date_start[0], My_eclipse_date_start[1].lower(), My_eclipse_date_start[2]
            My_eclipse_date_end = myEclipse[1].split(" ")
            My_eclipse_date_end = My_eclipse_date_end[0], My_eclipse_date_end[1].lower(), My_eclipse_date_end[2]
            a = False
            for eclipse in eclipses_dict:
                eclipse_date = eclipse[1], eclipse[2].lower(), eclipse[3] #('2000', 'Dec', '25')
                if eclipse_date == My_eclipse_date_start:
                    a = True
                    eclipses_dict.remove(eclipse)
                    break
                elif eclipse_date == My_eclipse_date_end:
                    a = True
                    eclipses_dict.remove(eclipse)
                    secondOptionCounter += 1
                    break
                else:
                    pass
            if a == True:
                trueCounter +=1
            else:
                false_eclipse_dates.append(My_eclipse_date_start)
                print(f"MyEclipseDate: {' '.join(My_eclipse_date_start)}")
                falseCounter +=1     
        summary = trueCounter+falseCounter
        print(f"True: {int(trueCounter/summary*100)}%, False: {int(falseCounter/summary*100)}%")
        print(f"Amount of untracked eclipses: {len(eclipses_dict)}, Second Option Counter: {secondOptionCounter}\n")
        
        return false_eclipse_dates, eclipses_dict
def print_all_dates(dates):
    for date in dates:
        date = " ".join(date)
        print(date)

def compare_all(filesNames):
    century = 19
    for file in filesNames:
        false_eclipses, not_tracked_eclipses = compare_by_century(century, file)
        century +=1
        # print_all_dates(false_eclipses)
        # print_all_dates(not_tracked_eclipses)

files = ("1901-2000.csv","2001-2100.csv","2101-2200.csv")
compare_all(files)

    