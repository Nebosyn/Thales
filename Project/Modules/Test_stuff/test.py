import datetime

def createEclipsesDictionary(eclipses_list):
    eclipses_dictionary = {}
    for eclipse in eclipses_list:
        eclipsestrp_start = datetime.datetime.strptime(eclipse[0],"%Y %b %d %H:%M:%S")  
        eclipsestrp_end = datetime.datetime.strptime(eclipse[1],"%Y %b %d %H:%M:%S")  
        # print(eclipsestrp_start)
        year_century = str(eclipsestrp_start.year)[:-2]
        print(str(eclipsestrp_start.year)[-1])
        if str(eclipsestrp_start.year)[-1] == "0":
            year_century = str(int(year_century)-1)
        print(year_century)
        if year_century not in eclipses_dictionary.keys():
            eclipses_dictionary[year_century] = []
        eclipses_dictionary[year_century].append(eclipse)
    return eclipses_dictionary

a = [["2000 FEB 05 10:59:45", "2000 FEB 05 14:42:01"], ["2000 JUL 01 18:13:36", "2000 JUL 01 20:52:47"], ["2000 JUL 31 00:41:34", "2000 JUL 31 03:47:09"], ["2000 DEC 25 15:32:19", "2000 DEC 25 19:40:05"]]

b = createEclipsesDictionary(a)
print(b)